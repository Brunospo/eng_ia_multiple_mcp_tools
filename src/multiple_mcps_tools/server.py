from fastapi import FastAPI, HTTPException, status
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field

from multiple_mcps_tools.graph.factory import build_graph


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=10)


def create_app() -> FastAPI:
    app = FastAPI()

    @app.post("/chat")
    async def chat_endpoint(body: ChatRequest):
        try:
            graph = await build_graph()

            response = await graph.ainvoke(
                {"messages": [HumanMessage(content=body.question)]}
            )

            if isinstance(response, dict):
                answer = (
                    response.get("answer")
                    or (
                        response.get("messages")[-1].content
                        if response.get("messages")
                        else None
                    )
                    or "No response generated."
                )
            else:
                # Se o objeto retornado for um objeto customizado
                answer = getattr(response, "answer", None) or "No response generated."

            return {"response": answer}

        except Exception as error:
            print(f"❌ Error processing request: {error}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing your request.",
            )

    return app
