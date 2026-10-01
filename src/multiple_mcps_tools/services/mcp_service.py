from langchain_mcp_adapters.client import MultiServerMCPClient

from multiple_mcps_tools.tools.mongodb_tool import get_mongodb_tool


async def get_mcp_tools():
    client = MultiServerMCPClient({**get_mongodb_tool()})

    mcp_tools = await client.get_tools()
    return [*mcp_tools]
