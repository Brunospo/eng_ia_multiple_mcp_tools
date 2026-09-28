from multiple_mcps_tools.graph.graph import build_chat_graph
from multiple_mcps_tools.services.open_router_service import OpenRouterService


async def build_graph():
    llm = OpenRouterService()
    return build_chat_graph(llm)


async def graph():
    return await build_graph()
