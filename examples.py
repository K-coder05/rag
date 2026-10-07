import json
import pathlib

EXAMPLE_QUESTIONS = [
	"How do I get startup ideas?",
	"What does PG say about fundraising?",
	"List essays about founders",
]
EXAMPLES_PATH = pathlib.Path(__file__).parent / "example_answers.json"


def normalize(question: str) -> str:
	return " ".join(question.lower().strip().rstrip("?.!").split())


def load_cached_answers() -> dict:
	# {normalized question: history entry} -- sources come back as Records so the
	# app renders them exactly like a live answer
	from main import Record

	if not EXAMPLES_PATH.exists():
		return {}
	with open(EXAMPLES_PATH, encoding="utf-8") as fp:
		entries = json.load(fp)

	cache = {}
	for question, entry in entries.items():
		entry["sources"] = [Record(**source) for source in entry["sources"]]
		cache[normalize(question)] = entry
	return cache


def answer_with_trace(query: str, max_iterations: int = 5) -> dict:
	# same loop as app.py, minus the streaming UI, so cached answers match live ones
	from main import client, tools, retrieve_context, format_records, list_topics, MODEL, AGENT_SYSTEM_PROMPT

	sources = []
	tool_trace = []

	def search_essays(query: str, top_k: int = 3) -> str:
		records = retrieve_context(query=query, top_k=top_k)
		sources.extend(records)
		return format_records(records)

	tool_functions = {"search_essays": search_essays, "list_topics": list_topics}
	messages = [{"role": "user", "content": query}]

	for _ in range(max_iterations):
		response = client.messages.create(
			model=MODEL,
			max_tokens=2000,
			tools=tools,
			messages=messages,
			system=AGENT_SYSTEM_PROMPT,
		)
		text = "".join(block.text for block in response.content if block.type == "text")

		if response.stop_reason != "tool_use":
			return {"role": "assistant", "content": text, "tool_calls": tool_trace, "sources": sources}

		reason = text.strip() or "(no explanation given)"
		messages.append({"role": "assistant", "content": response.content})

		tool_results = []
		for block in response.content:
			if block.type != "tool_use":
				continue
			tool_trace.append({"name": block.name, "input": block.input, "reason": reason})
			tool_results.append({
				"type": "tool_result",
				"tool_use_id": block.id,
				"content": tool_functions[block.name](**block.input),
			})
		messages.append({"role": "user", "content": tool_results})

	raise RuntimeError(f"agent did not finish within {max_iterations} iterations: {query!r}")


if __name__ == "__main__":
	# python examples.py -- regenerates example_answers.json (commit the output)
	from main import load_bm25_corpus

	load_bm25_corpus()
	entries = {}
	for question in EXAMPLE_QUESTIONS:
		print(f"Answering: {question}")
		entry = answer_with_trace(question)
		entry["sources"] = [vars(record) for record in entry["sources"]]
		entries[question] = entry

	with open(EXAMPLES_PATH, "w", encoding="utf-8") as fp:
		json.dump(entries, fp, ensure_ascii=False, indent=2)
	print(f"Wrote {EXAMPLES_PATH}")
