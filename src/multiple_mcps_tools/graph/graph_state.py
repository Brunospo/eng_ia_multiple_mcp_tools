from collections.abc import Sequence
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages


class GraphState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

    answer: str | None
    intent: str | None
    file_content: str | None
    file_name: str | None
    error: str | None
