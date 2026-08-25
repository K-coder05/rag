import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from anthropic import Anthropic

load_dotenv()

embeddings_model = GoogleGenerativeAIEmbeddings(
	model='gemini-embedding-001',
	task_type='RETRIEVAL_QUERY'
)

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
index = pc.Index("startup-library")

class Record:
	def __init__(self, ID: str = "", score: float = 0.0, text: str = "", source: str = "") -> None:
		self.ID = ID
		self.score = score
		self.text = text
		self.source = source

def retrieve(query: str, top_k: int = 3) -> list[Record]:
	query_vector = embeddings_model.embed_query(query)
	results = index.query(
		vector=query_vector,
		top_k=top_k,
		include_metadata=True,
		namespace="startup-library"
	)

	records = []
	for match in results["matches"]:
		ID = match["id"]
		score = match["score"]
		text = match["metadata"].get('text', '')
		source = match["metadata"].get('source', '')

		record = Record(ID = ID, score=score, text=text, source=source)
		records.append(record)

	return records


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