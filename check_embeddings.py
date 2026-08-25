import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

embeddings_model = GoogleGenerativeAIEmbeddings(
	model='gemini-embedding-001',
	task_type='RETRIEVAL_QUERY'
)

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
index = pc.Index("startup-library")

def check_embeddings(query_text: str, top_k: int = 3):
	print(f"Running checks for query: '{query_text}' ---")

	query_vector = embeddings_model.embed_query(query_text)
	results = index.query(
		vector=query_vector,
		top_k=top_k,
		include_metadata=True,
		namespace="startup-library"
	)

	for i, match in enumerate(results["matches"], start=1):
		print(f"\nRank {i}:")
		print(f"-- ID: {match['id']}")
		print(f"-- Similarity Score: {match['score']:.4f}")
		if match.get("metadata"):
			text_preview = match['metadata'].get('text', '')[:200].replace('\n', ' ')
			print(f"Preview: {text_preview}...")
			print(f"Source: {match['metadata'].get('source', 'N/A')}")


if __name__ == "__main__":
	check_embeddings("How to get startup ideas and find problems to solve")
	check_embeddings("How to find new business ideas for a startup")