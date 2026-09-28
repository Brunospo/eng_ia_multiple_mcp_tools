from langchain.messages import AIMessage

from multiple_mcps_tools.graph.graph_state import GraphState
from multiple_mcps_tools.services.open_router_service import OpenRouterService


def intent_node(open_router_service: OpenRouterService):
    async def create_intent_node(state: GraphState):
        print("🧠 Intent node processing...")

        try:
            raw_question = state.get("messages")[-1].text
            return {"intent": "", "file_content": "{}", "file_name": "report.json"}
        except Exception as error:
            print(f"Intent node error: {error}")
            return {
                "error": str(error),
                "messages": [
                    AIMessage(
                        content="Sorry, I had trouble understanding the intent. Please rephrase your question or provide more details."
                    )
                ],
            }

    return create_intent_node
