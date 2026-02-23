import fastmcp

from tools import register_tools

mcp = fastmcp.FastMCP(
    "Meteor.js Documentation",
    instructions="MCP server providing complete Meteor.js v3.4.0 API documentation, code examples, and architectural guides.",
)

register_tools(mcp)

if __name__ == "__main__":
    mcp.run(transport="stdio")
