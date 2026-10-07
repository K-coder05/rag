# Startup Library Assistant

A retrieval-augmented agent over Paul Graham's essays and the YC Startup Library. Given a question, it decides whether to search the corpus or list browsable topics, retrieves context with a hybrid dense + BM25 pipeline, and answers strictly from what it retrieves. Built to compare RAG design choices (chunking, one-pass retrieval vs. an agentic tool-calling loop) with a small hand-written eval set scored LLM-as-judge style.

## Demo

## Architecture Design

### Ingestion (`injection_script.py`)
- YC Combinator and Paul Graham's essays as corpus
- Google's gemini-embedding-001 model to create embeddings
- Pinecone database to store embeddings

### Retrieval and Generation (`main.py`)
- Google's gemini-embedding-001 model for standard vector search & retrieval
- Keyword/BM25 search to pair with ^ for Reciprocal Rank Fusion
- Anthropic's claude-haiku-4-5 for response generation

### Agent Loop and Tools
- The agent (`main.py`, and the Streamlit UI in `app.py`) chooses between two tools each turn: `search_essays` or `list_topics`
- `mcp_server.py` separately exposes those same two functions over the MCP protocol, for use by external MCP clients (e.g. Claude Desktop) — it's independent of the agent loop above, which calls the tool functions directly rather than over MCP

### Evals/Tracing
- Raw testing transcripts found in transcripts/, one folder per tested strategy
- Tested one-pass RAG vs. agentic loop and databases made using varying chunk size and larger overlap
- Evaluations (LLM as a judge, tool usage accuracy) found on [Spreadsheet](https://docs.google.com/spreadsheets/d/1hyEVvpAo-MYJM3A43c-CUo1Hd3xRI01FvHSbk6QdTOs/edit?gid=0#gid=0)

<!-- TODO: paste inline eval results (a summary table of the key metrics/findings) here -->

## Project Structure

| Path | Purpose |
|---|---|
| `main.py` | Retrieval + generation pipeline and the ReAct agent loop; CLI entry point |
| `app.py` | Streamlit chat UI on top of the same agent loop — streamed answers, tool-call trace, sources panel |
| `examples.py` | Example questions shown on the empty chat; `python examples.py` regenerates their cached answers |
| `example_answers.json` | Pre-computed answers for the example questions, so a first click answers instantly |
| `injection_script.py` | Chunks the corpus, embeds it, upserts into Pinecone |
| `check_embeddings.py` | Manual sanity check of retrieval quality against the index |
| `tools.py` | Anthropic tool schema definitions used by the agent |
| `mcp_server.py` | Exposes `search_essays`/`list_topics` via the MCP protocol |
| `scrape_pg_essays.py`, `scrape_yc_library.py` | Corpus collection scripts |
| `testing.py` | Runs `eval_set.json` against each strategy, writes transcripts |
| `eval_set.json` | Hand-written eval questions with expected answers/sources/tool choice |
| `corpus/` | Scraped source documents (`pg_essays/`, `yc_library/`) |
| `transcripts/` | Raw eval run outputs, one folder per tested strategy |

## Setup

Prerequisites: Python 3.11+, an Anthropic API key, a Google AI (Gemini) API key, and a Pinecone API key.

- clone the repository and cd into the new directory (with new virtual environment)
- run "pip install -r requirements.txt" in your terminal
- add the necessary API keys (see .env.example / table below)
- run scraper and injection Python files (run "python ...") to build the corpus and populate the Pinecone index
  - ingestion also writes `chunks/<namespace>.json`, which `main.py` loads at startup to build the BM25 index (no Pinecone round-trips); for a namespace ingested before this file existed, run "python injection_script.py --export-chunks startup-library startup-library-v2" once and commit the output
- run "streamlit run app.py" in your terminal
  - or use the CLI directly: "python main.py"

### Environment variables

| Variable | Used by |
|---|---|
| `ANTHROPIC_API_KEY` | `main.py`, `app.py` (response generation) |
| `GEMINI_API_KEY` | `injection_script.py`, `main.py`, `check_embeddings.py` (embeddings) |
| `PINECONE_API_KEY` | `injection_script.py`, `main.py`, `check_embeddings.py` (vector store) |

### Reproduce Evals
- run "python testing.py"
