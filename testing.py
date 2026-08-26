import json
import time
import pathlib
import datetime

import main
from main import ask

STRATEGIES = [
	{"name": "agent_baseline", "namespace": "startup-library"},
	{"name": "agent_v2", "namespace": "startup-library-v2"},
]

with open("eval_set.json", encoding="utf-8") as f:
	eval_items = json.load(f)

tool_call_log = []

def _tracking_wrapper(name, real_fn):
	def wrapped(**kwargs):
		output = real_fn(**kwargs)
		tool_call_log.append({"tool": name, "input": kwargs, "output": output})
		return output
	return wrapped

main.search_essays = _tracking_wrapper("search_essays", main.search_essays)
main.list_topics = _tracking_wrapper("list_topics", main.list_topics)

for strategy in STRATEGIES:
	main.NAMESPACE = strategy["namespace"]
	main.load_bm25_corpus.cache_clear()

	out_dir = pathlib.Path("transcripts") / strategy["name"]
	out_dir.mkdir(parents=True, exist_ok=True)

	for item in eval_items:
		tool_call_log.clear()

		before = time.perf_counter()
		response = ask(query=item["query"])
		after = time.perf_counter()

		filename = out_dir / (datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".json")
		transcript = {
			"strategy": strategy["name"],
			"id": item.get("id"),
			"query": item["query"],
			"category": item.get("category"),
			"expected_answer": item.get("expected_answer"),
			"expected_sources": item.get("expected_sources"),
			"expected_tool_choice": item.get("expected_tool_choice"),
			"tool_calls": list(tool_call_log),
			"response": response,
			"response_time": after - before,
		}
		with open(file=filename, mode="w", encoding="utf-8") as fp:
			json.dump(transcript, fp, indent=2)
