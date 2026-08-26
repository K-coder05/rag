from mcp.server.mcpserver import MCPServer
from main import search_essays, list_topics

mcp = MCPServer(name="startup-library")
mcp.tool()(search_essays)
mcp.tool()(list_topics)

if __name__ == "__main__": mcp.run()
