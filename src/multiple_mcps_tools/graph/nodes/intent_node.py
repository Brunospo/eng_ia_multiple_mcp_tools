from langchain.messages import AIMessage

from multiple_mcps_tools.graph.graph_state import GraphState
from multiple_mcps_tools.prompts.v1.identify_intent import (
    IntentSchema,
    get_system_prompt,
)
from multiple_mcps_tools.services.open_router_service import OpenRouterService


def intent_node(open_router_service: OpenRouterService):
    async def create_intent_node(state: GraphState):
        print("🧠 Intent node processing...")

        try:
            raw_question = state.get("messages")[-1].text
            system_prompt = get_system_prompt()

            result = await open_router_service.generate_structured(
                system_prompt, raw_question, IntentSchema
            )

            data: IntentSchema = result.get("data")

            if not data.intent or not data.file_type:
                print("⚠️ Missing intent or fileType in data.", data)
                raise Exception("Invalid intent data")

            # Equivalente ao operador ??= (atribuição se for None)
            if data.file_name is None:
                data.file_name = f"data.{data.file_type}"

            print("📋 Extracted intent:", data.intent)
            print("📄 File Type:", data.file_type)
            print("📄 File name:", data.file_name)

            return {
                "intent": data.intent,
                "file_content": data.file_content or "",
                "file_name": data.file_name,
            }
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
