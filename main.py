import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from anthropic import Anthropic
from rank_bm25 import BM25Okapi

load_dotenv()

embeddings_model = GoogleGenerativeAIEmbeddings(
	model='gemini-embedding-001',
	task_type='RETRIEVAL_QUERY'
)

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
index = pc.Index("startup-library")

class Record:
	def __init__(self, id: str = "", score: float = 0.0, text: str = "", source: str = "") -> None:
		self.id = id
		self.score = score
		self.text = text
		self.source = source

def tokenize(text: str) -> list[str]:
	return text.lower().split()

def retrieve(query: str, n: int = 3) -> list[Record]:
	# standard vector search
	query_vector = embeddings_model.embed_query(query)
	results = index.query(
		vector=query_vector,
		top_k=n,
		include_metadata=True,
		namespace="startup-library"
	)

	doc_lookup = {}
	records = []
	for match in results["matches"]:
		id = match["id"]
		score = match["score"]
		text = match["metadata"].get('text', '')
		source = match["metadata"].get('source', '')

		record = Record(id = id, score=score, text=text, source=source)
		records.append(record)
		doc_lookup[id] = {"text" : text, "source" : source}

	# keyword/BM25 search alongside vector search
	IDs = []
	pages = index.list(namespace="startup-library")
	for page in pages:
		for vector in page.vectors:
			IDs.append(vector.id)

	fetches = {}
	batch_size = 100
	for start in range(0, len(IDs), batch_size):
		fetch = index.fetch(ids=IDs[start:start+batch_size], namespace="startup-library")
		fetches.update(fetch.vectors)

	documents = []
	texts = []
	for vector in fetches.values():
		if vector.metadata:
			texts.append(tokenize(vector.metadata["text"]))
			document = {
				"id" : vector.id,
				"source" : vector.metadata["source"],
				"text" : vector.metadata["text"]
			}

			documents.append(document)
			doc_lookup[document["id"]] = {"text" : document["text"], "source" : document["source"]}

	ranker = BM25Okapi(corpus=texts, tokenizer=None, k1=1.5, b=0.65, epsilon=0.25)
	tokenized_query = tokenize(query)
	ranks = ranker.get_top_n(tokenized_query, documents=documents, n=n)

	# fuse for Reciprocal Rank Fusion usings 'ranks' and 'records'
	k = 60
	dense_rank = {}
	for i in range(len(records)):
		dense_rank[records[i].id] = i + 1

	bm25_rank = {}
	for i in range(len(ranks)):
		bm25_rank[ranks[i]["id"]] = i + 1

	record_ids = [record.id for record in records]
	rank_ids = [document["id"] for document in ranks]
	union_ids = list(set(record_ids).union(set(rank_ids)))

	final_scores = {}
	for id in union_ids:
		rrf_score = 0
		if id in record_ids:
			rrf_score += 1 / (k + dense_rank[id])
		if id in rank_ids:
			rrf_score += 1 / (k + bm25_rank[id])
		final_scores[id] = rrf_score

	final_ids = sorted(final_scores, key=lambda id: final_scores[id], reverse=True)[:n]

	final_records = []
	for id in final_ids:
		text = doc_lookup[id]["text"]
		source = doc_lookup[id]["source"]
		score = final_scores[id]

		record = Record(id=id, score=score, text=text, source=source)
		final_records.append(record)

	return final_records


def generate(query, records: list[Record]) -> str:
	client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
	prompt = f"""
		You are an experienced startup founder that researched the field of startups for years.
		Respond to this question: '{query}' by citing these top relevant sources you have found.
	"""

	for i in range(min(5, len(records))):
		prompt += f"From source {records[i].source}: {records[i].text}\n\n"

	response = client.messages.create(
		model="claude-haiku-4-5",
		max_tokens=2000,
		system="only answer from context",
		messages=[{"role": "user", "content": prompt}]
	)

	res = ""
	for block in response.content:
		if block.type == "text":
			res += block.text

	return res

if __name__ == "__main__":
	try:
		while True:
			query = input("Ask away ('quit' or 'exit' to leave): ")
			if query.lower() in ("quit", "exit"):
				break

			try:
				print("--- Retrieval Process ---")
				records = retrieve(query=query)
				for record in records:
					print(f"Source: {record.source}")
					print(f"Score: {record.score}")
					text_preview = record.text[:200].replace('\n', ' ')
					print(f"Preview: {text_preview}...")
			except Exception as e:
				print(f"Retrieval failed: {type(e).__name__} -- {e}")
				continue
			try:
				print("--- Generate Process ---")
				response = generate(query=query, records=records)
				print(f"Response: {response}")
			except Exception as e:
				print(f"Generation failed: {type(e).__name__} -- {e}")
				continue

	except KeyboardInterrupt:
		print("Stopped sporadically.")