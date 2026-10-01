from langchain.messages import AIMessage

from multiple_mcps_tools.graph.graph_state import GraphState
from multiple_mcps_tools.prompts.v1.agent_node import get_system_prompt, get_user_prompt
from multiple_mcps_tools.services.open_router_service import OpenRouterService


def agent_node(open_router_service: OpenRouterService):
    async def create_agent_node(state: GraphState):
        print("🤖 Agent node processing...")

        try:
            user_message = get_user_prompt(
                state.get("intent"), state.get("file_name"), state.get("file_content")
            )

            result = await open_router_service.generate_structured(
                get_system_prompt(), user_message
            )

            return {"messages": AIMessage(result.get("data"))}
        except Exception as error:
            print(f"Agent error: {error}")
            return {
                "error": str(error),
                "messages": [
                    AIMessage(content="Sorry, I had trouble processing the request.")
                ],
            }

    return create_agent_node
