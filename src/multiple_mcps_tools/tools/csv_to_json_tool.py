import csv
import json
from io import StringIO

from langchain_core.tools import tool
from pydantic import Field


@tool
def csv_to_json(
    csvText: str = Field(description="CSV data to be converted to JSON format"),
) -> str:
    """Convert CSV format to JSON"""
    # Lê a string de texto CSV usando StringIO
    f = StringIO(csvText)
    reader = csv.DictReader(f)
    result = list(reader)

    print(f"[getCSVToJSONTool] conversion result finished {len(result)} records")

    return json.dumps(result, ensure_ascii=False)
