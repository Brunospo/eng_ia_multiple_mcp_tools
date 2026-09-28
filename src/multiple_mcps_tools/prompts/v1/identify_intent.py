from typing import Literal

from pydantic import BaseModel, Field


class IntentSchema(BaseModel):
    intent: str = Field(
        ...,
        description=(
            "A clean, concise natural-language description of what the user"
            " wants to accomplish. Do NOT include any CSV or JSON data in this"
            " field."
        ),
    )
    file_content: str | None = Field(
        None,
        description=(
            "The raw CSV or JSON block embedded in the message, exactly as"
            " provided. If there is no file content, set this to null."
        ),
    )
    file_name: str | None = Field(
        None,
        description=(
            'An inferred filename or type for the data (e.g. "sales", "report").'
            " Derive it from the question."
        ),
    )
    file_type: Literal["csv", "json", "unknown"] = Field(
        ...,
        description=(
            "The inferred file type based on the content or filename. If it looks"
            ' like CSV, set to "csv". If it looks like JSON, set to "json".'
            ' Otherwise, set to "unknown".'
        ),
    )


def get_system_prompt() -> str:
    return """
You are an intent extraction assistant.
Analyze the user message and extract the requested fields as structured output.
The user message may contain a natural-language instruction mixed with raw file content (CSV or JSON).
Separate them cleanly: the intent is the goal, file_content is the raw data block, file_name is the inferred file name.
If no file data is present, set file_content and file_name to null.
""".strip()
