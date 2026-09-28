from langchain.messages import AIMessage

from multiple_mcps_tools.graph.graph_state import GraphState
from multiple_mcps_tools.services.open_router_service import OpenRouterService


def agent_node(open_router_service: OpenRouterService):
    async def create_agent_node(state: GraphState):
        print("🤖 Agent node processing...")

        try:
            return {"messages": AIMessage("Nothing yet")}
        except Exception as error:
            print(f"Agent error: {error}")
            return {
                "error": str(error),
                "messages": [
                    AIMessage(content="Sorry, I had trouble processing the request.")
                ],
            }

    return create_agent_node
