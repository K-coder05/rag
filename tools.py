tools = [
	{
		"name" : "search_essays",
		"description" : "Call this when the user asks a question likely answered by the essay/library content",
		"input_schema" : {
			"type" : "object",
			"properties" : {
				"query" : {
					"type" : "string",
					"description" : "the question the user is asking"
				},
				"top_k" : {
					"type" : "integer",
					"description" : "number of relevant sources to retrieve"
				}
			},
			"required" : ["query"]
		}
	},
	{
		"name" : "list_topics",
		"description" : "Call this when the user wants a browsable list of topics/titles rather than a specific answer",
		"input_schema" : {
			"type" : "object",
			"properties" : {
				"query" : {
					"type" : "string",
					"description" : "optional keyword filter"
				}
			}
		}
	}
]