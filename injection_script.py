import hashlib
import json
import os
import pathlib
import sys
import time

from google.genai.errors import ClientError
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

load_dotenv()

CORPUS_DIRS = ("corpus/pg_essays", "corpus/yc_library")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "startup-library")
NAMESPACE = os.getenv("PINECONE_NAMESPACE", "startup-library-v2")
CHUNKS_DIR = pathlib.Path(__file__).parent / "chunks"
EMBEDDING_DIMENSION = 3072
EMBED_BATCH_SIZE = 100
EMBED_BATCH_DELAY_SECONDS = float(os.getenv("EMBED_BATCH_DELAY_SECONDS", "2"))


def _is_rate_limit_error(exc: BaseException) -> bool:
	cause = exc.__cause__
	return isinstance(cause, ClientError) and cause.code == 429


@retry(
	retry=retry_if_exception(_is_rate_limit_error),
	wait=wait_exponential(multiplier=2, min=5, max=120),
	stop=stop_after_attempt(8),
	reraise=True,
)
def _embed_batch(embeddings_model, texts):
	return embeddings_model.embed_documents(texts)


def embed_all(embeddings_model, texts):
	vectors = []
	for start in range(0, len(texts), EMBED_BATCH_SIZE):
		batch = texts[start:start + EMBED_BATCH_SIZE]
		vectors.extend(_embed_batch(embeddings_model, batch))
		time.sleep(EMBED_BATCH_DELAY_SECONDS)
	return vectors


def load_markdown_documents():
	documents = []
	for corpus_dir in CORPUS_DIRS:
		loader = DirectoryLoader(
			corpus_dir,
			glob="**/*.md",
			loader_cls=TextLoader,
			loader_kwargs={"encoding": "utf-8"},
		)
		documents.extend(loader.load())
	return documents


def main():
	if not os.getenv("GEMINI_API_KEY"):
		raise RuntimeError("GEMINI_API_KEY is missing from .env")
	if not os.getenv("PINECONE_API_KEY"):
		raise RuntimeError("PINECONE_API_KEY is missing from .env")

	documents = load_markdown_documents()
	if not documents:
		raise RuntimeError("No markdown documents found in the corpus directories")

	headers_to_split_on = [
		("#", "Header 1"),
		("##", "Header 2"),
		("###", "Header 3"),
	]
	markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

	final_chunks = []
	# baseline is 1000 size, 200 overlap; v2 is 1250 size, 250 overlap
	text_splitter = RecursiveCharacterTextSplitter(chunk_size=1250, chunk_overlap=250)

	for doc in documents:
		header_splits = markdown_splitter.split_text(doc.page_content)
		splits = text_splitter.split_documents(header_splits)
		for split in splits:
			split.metadata["source"] = doc.metadata.get("source")
			final_chunks.append(split)

	embeddings_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
	vectors = embed_all(embeddings_model, [chunk.page_content for chunk in final_chunks])

	pinecone = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
	if not pinecone.has_index(INDEX_NAME):
		pinecone.create_index(
			name=INDEX_NAME,
			dimension=EMBEDDING_DIMENSION,
			metric="cosine",
			spec=ServerlessSpec(cloud="aws", region="us-east-1"),
		)
	index = pinecone.Index(INDEX_NAME)

	records = []
	for chunk, vector in zip(final_chunks, vectors):
		source = chunk.metadata.get("source", "")
		chunk_id = hashlib.sha256(f"{source}:{chunk.page_content}".encode()).hexdigest()
		records.append({
			"id": chunk_id,
			"values": vector,
			"metadata": {
				"text": chunk.page_content,
				"source": source,
			},
		})

	batch_size = 100
	for start in range(0, len(records), batch_size):
		index.upsert(vectors=records[start:start + batch_size], namespace=NAMESPACE)

	# local copy of the chunk texts so main.py can build BM25 without hitting Pinecone
	# (keyed by id since duplicate chunks collapse to one vector in Pinecone too)
	unique_chunks = {record["id"]: {"id": record["id"], **record["metadata"]} for record in records}
	chunks = sorted(unique_chunks.values(), key=lambda chunk: chunk["id"])
	CHUNKS_DIR.mkdir(exist_ok=True)
	with open(CHUNKS_DIR / f"{NAMESPACE}.json", "w", encoding="utf-8") as fp:
		json.dump(chunks, fp, ensure_ascii=False)

	print(f"Embedded and upserted {len(records)} chunks into '{INDEX_NAME}/{NAMESPACE}'.")


if __name__ == "__main__":
	if sys.argv[1:2] == ["--export-chunks"]:
		# one-time dump of already-ingested namespaces: python injection_script.py --export-chunks ns1 ns2
		from main import export_chunks_from_pinecone
		for namespace in sys.argv[2:] or [NAMESPACE]:
			print(f"Exported {len(export_chunks_from_pinecone(namespace))} chunks from '{namespace}'.")
	else:
		main()
