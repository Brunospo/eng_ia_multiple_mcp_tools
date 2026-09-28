import json
from dataclasses import asdict
from typing import Any, TypeVar
from uuid import UUID

from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy
from langchain_core.callbacks import AsyncCallbackHandler
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.outputs import LLMResult
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from multiple_mcps_tools.config import ModelConfig, config
from multiple_mcps_tools.services.mcp_service import get_mcp_tools

T = TypeVar("T", bound=BaseModel)


class LoggingCallbackHandler(AsyncCallbackHandler):
    async def on_chat_model_start(self, serialized, messages, **kwargs) -> None:
        last_msg = messages[-1][-1] if messages and messages[-1] else None
        print("\n🧠 LLM thinking...")
        print(f' (last message: "{last_msg.content if last_msg else None}")')

    async def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        try:
            msg = response.generations[0][0].message
            tool_calls = getattr(msg, "tool_calls", None)
            if tool_calls:
                names = ", ".join(t["name"] for t in tool_calls)
                print(f"🎯 Decided to call: {names}")
        except (IndexError, AttributeError):
            pass

    async def on_tool_start(
        self,
        serialized: dict[str, Any],
        input_str: str,
        *,
        run_id: UUID,
        name: str | None = None,
        **kwargs,
    ) -> None:
        print(f"🔧 Tool called: {name} →", input_str)

    async def on_tool_end(
        self,
        output: Any,
        *,
        run_id: UUID,
        name: str | None = None,
        **kwargs,
    ) -> None:
        print(f"✅ Tool done:   {name} →", output)


class OpenRouterService:
    _config: ModelConfig
    _llm_client: ChatOpenAI
    _tools: list[Any]

    def __init__(self, config_override: ModelConfig | None = None) -> None:
        self._config = config_override or config
        self._tools = []

        self._llm_client = ChatOpenAI(
            model=self._config.models[0],
            temperature=self._config.temperature,
            openai_api_key=self._config.api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            max_tokens=self._config.max_tokens,
            default_headers={
                "HTTP-Referer": self._config.http_referer,
                "X-Title": self._config.x_title,
            },
            extra_body={"provider": asdict(self._config.provider)},
        )

    async def _get_tools(self) -> list:
        if not self._tools:
            self._tools = await get_mcp_tools()

        return self._tools

    async def generate_structured(
        self, system_prompt: str, user_prompt: str, schema: type[T] | None = None
    ):
        try:
            if schema:
                agent = create_agent(
                    model=self._llm_client,
                    tools=[],
                    response_format=ProviderStrategy(schema),
                )
            else:
                agent = create_agent(
                    model=self._llm_client,
                    tools=await self._get_tools(),
                )

            messages = [SystemMessage(system_prompt), HumanMessage(user_prompt)]

            data = await agent.ainvoke(
                {"messages": messages}, config={"callbacks": [LoggingCallbackHandler()]}
            )

            print(
                "✅ LLM Response:",
                json.dumps(data, indent=2, default=str, ensure_ascii=False),
            )

            if schema:
                result = data["structured_response"]
            else:
                result = data["messages"][-1].text if data["messages"] else ""

            return {"data": result}

        except Exception as error:
            print(f"Error OpenRouterService: {error}")

            return {"success": False, "error": str(error)}
