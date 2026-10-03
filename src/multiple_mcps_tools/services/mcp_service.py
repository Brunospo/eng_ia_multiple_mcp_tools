from langchain_mcp_adapters.client import MultiServerMCPClient

from multiple_mcps_tools.tools.csv_to_json_tool import csv_to_json
from multiple_mcps_tools.tools.fs_tool import get_fs_tool
from multiple_mcps_tools.tools.mongodb_tool import get_mongodb_tool


async def get_mcp_tools():
    client = MultiServerMCPClient({**get_mongodb_tool(), **get_fs_tool()})

    mcp_tools = await client.get_tools()
    return [*mcp_tools, csv_to_json]
