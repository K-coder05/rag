import os
import functools
from dotenv import load_dotenv
import pathlib
import frontmatter

from pinecone import Pinecone
from rank_bm25 import BM25Okapi

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from anthropic import Anthropic

from tools import tools

CORPUS_DIRS = ("corpus/pg_essays", "corpus/yc_library")
NAMESPACE = "startup-library"
CONSTANT_K = 60


# load environment variables
load_dotenv()

# Gemini model for retrieval
embeddings_model = GoogleGenerativeAIEmbeddings(
	model='gemini-embedding-001',
	task_type='RETRIEVAL_QUERY'
)

# PineCone database
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
index = pc.Index(NAMESPACE)

# Anthropic model for generation
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

class Record:
	def __init__(self, id: str = "", score: float = 0.0, text: str = "", source: str = "") -> None:
		self.id = id
		self.score = score
		self.text = text
		self.source = source

def tokenize(text: str) -> list[str]:
	return text.lower().split()

@functools.lru_cache(maxsize=1)
def load_bm25_corpus():
	IDs = []
	pages = index.list(namespace=NAMESPACE)
	for page in pages:
		for vector in page.vectors:
			IDs.append(vector.id)

	fetches = {}
	batch_size = 100
	for start in range(0, len(IDs), batch_size):
		fetch = index.fetch(ids=IDs[start:start+batch_size], namespace=NAMESPACE)
		fetches.update(fetch.vectors)

	documents = []
	texts = []
	doc_lookup = {}
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
	return ranker, documents, doc_lookup


def retrieve_context(query: str, top_k: int = 3) -> list[Record]:
	# standard vector search
	query_vector = embeddings_model.embed_query(query)
	results = index.query(
		vector=query_vector,
		top_k=top_k,
		include_metadata=True,
		namespace=NAMESPACE
	)

	records = []
	for match in results["matches"]:
		id = match["id"]
		score = match["score"]
		text = match["metadata"].get('text', '')
		source = match["metadata"].get('source', '')

		record = Record(id = id, score=score, text=text, source=source)
		records.append(record)

	# keyword/BM25 search alongside vector search -- corpus and ranker are cached
	ranker, documents, doc_lookup = load_bm25_corpus()
	tokenized_query = tokenize(query)
	ranks = ranker.get_top_n(tokenized_query, documents=documents, n=top_k)

	# fuse for Reciprocal Rank Fusion usings 'ranks' and 'records'
	dense_rank = {}
	for i in range(len(records)):
		dense_rank[records[i].id] = i + 1

	bm25_rank = {}
	for i in range(len(ranks)):
		bm25_rank[ranks[i]["id"]] = i + 1

	record_ids = {record.id for record in records}
	rank_ids = {document["id"] for document in ranks}
	union_ids = record_ids | rank_ids

	final_scores = {}
	for id in union_ids:
		rrf_score = 0
		if id in record_ids:
			rrf_score += 1 / (CONSTANT_K + dense_rank[id])
		if id in rank_ids:
			rrf_score += 1 / (CONSTANT_K + bm25_rank[id])
		final_scores[id] = rrf_score

	final_ids = sorted(final_scores, key=lambda id: final_scores[id], reverse=True)[:top_k]

	final_records = []
	for id in final_ids:
		text = doc_lookup[id]["text"]
		source = doc_lookup[id]["source"]
		score = final_scores[id]

		record = Record(id=id, score=score, text=text, source=source)
		final_records.append(record)

	return final_records

def format_records(records: list[Record]) -> str:
	result = ""
	for record in records:
		result += f"From source {record.source}: {record.text}\n\n"

	return result

# tools for model to choose from
def search_essays(query: str, top_k: int = 3) -> str:
	retrieved_records = retrieve_context(query=query, top_k=top_k)
	return format_records(retrieved_records)

@functools.lru_cache(maxsize=1)
def load_titles() -> tuple[str, ...]:
	# Reads and YAML-parses every corpus file -- query-independent, so it's
	# cached and only runs once instead of on every list_topics() call.
	titles = []
	for corpus_dir in CORPUS_DIRS:
		for file in pathlib.Path(corpus_dir).glob("**/*.md"):
			post = frontmatter.load(file)
			titles.append(str(post.metadata["title"]))
	return tuple(titles)


def list_topics(query: str = "") -> str:
	result = ""
	for title in load_titles():
		if not query or query.lower() in title.lower():
			result += title

	return result

# ReAct loop
def ask(query: str, max_iterations: int = 5) -> str:
	tool_functions = {
		"search_essays": search_essays,
		"list_topics": list_topics
	}
	messages = [{"role" : "user", "content" : query}]

	for _ in range(max_iterations):
		response = client.messages.create(
			model="claude-haiku-4-5",
			max_tokens=2000,
			tools=tools,
			messages=messages,
			system="answer only from context"
		)

		if response.stop_reason != "tool_use":
			res = ""
			for block in response.content:
				if block.type == "text":
					res += block.text
			return res

		messages.append({"role" : "assistant", "content" : response.content})

		tool_results = []
		for block in response.content:
			if block.type != "tool_use":
				continue
			try:
				output = tool_functions[block.name](**block.input)
				tool_results.append({
					"type" : "tool_result",
					"tool_use_id" : block.id,
					"content" : output
				})
			except Exception as e:
				tool_results.append({
					"type" : "tool_result",
					"tool_use_id" : block.id,
					"content" : str(e),
					"is_error" : True
				})

		messages.append({"role" : "user", "content" : tool_results})

	return "Sorry, I couldn't finish reasoning about this in time."

if __name__ == "__main__":
	try:
		while True:
			query = input("Ask away ('quit' or 'exit' to leave): ")
			if query.lower() in ("quit", "exit"):
				break

			try:
				response = ask(query=query)
				print(f"Response: {response}")
			except Exception as e:
				print(f"Agent failed: {type(e).__name__} -- {e}")
				continue

	except KeyboardInterrupt:
		print("Stopped sporadically.")