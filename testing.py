from main import retrieve, generate
import time
import pathlib
import json
import datetime

test_cases = []
test = {}
test["query"] = "What does Paul Graham mean by 'Do Things that Don't Scale'?"
test["category"] = "easy"
test_cases.append(test)

test = {}
test["query"] = "What is the difference between a maker's schedule and a manager's schedule?"
test["category"] = "easy"
test_cases.append(test)

test = {}
test["query"] = "Why does Paul Graham advise against starting a company with a single founder?"
test["category"] = "easy"
test_cases.append(test)

test = {}
test["query"] = "How does a founder's approach to user acquisition evolve between having 10 users versus having 10,000 users?"
test["category"] = "hard"
test_cases.append(test)

test = {}
test["query"] = "What qualities distinguish an idea that sounds bad but is actually good from an idea that is genuinely bad?"
test["category"] = "hard"
test_cases.append(test)

test = {}
test["query"] = "Compare the dynamics of raising angel funding versus venture capital as described across the essays."
test["category"] = "hard"
test_cases.append(test)

test = {}
test["query"] = "Why is high organic user retention more critical in the early stages than raw top-of-funnel acquisition?"
test["category"] = "hard"
test_cases.append(test)

test = {}
test["query"] = "What was the closing stock price of Apple on January 15, 2024?"
test["category"] = "out-of-scope"
test_cases.append(test)

test = {}
test["query"] = "What are the step-by-step instructions for calculating the Black-Scholes option pricing model in Python?"
test["category"] = "out-of-scope"
test_cases.append(test)

test = {}
test["query"] = "How do I configure an Nginx reverse proxy with SSL termination on Ubuntu 22.04?"
test["category"] = "out-of-scope"
test_cases.append(test)

path = pathlib.Path("transcripts")
path.mkdir(parents=True, exist_ok=True)

for test in test_cases:
	query = test["query"]
	category = test["category"]

	before_retrieval = time.perf_counter()
	records = retrieve(query=query)
	after_retrieval = time.perf_counter()
	chunks = []
	for record in records:
		chunks.append(vars(record))
	retrieval_time = after_retrieval - before_retrieval

	before_generation= time.perf_counter()
	response = generate(query=query, records=records)
	after_generation = time.perf_counter()
	generation_time = after_generation - before_generation

	filename = path / (datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".json")
	transcript = {
		"query": query,
		"category": category,
		"chunks": chunks,
		"retrieval_time": retrieval_time,
		"generation_time": generation_time,
		"response": response,
	}
	with open(file=filename, mode="w", encoding="utf-8") as fp:
		json.dump(transcript, fp, indent=2)