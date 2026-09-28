import sys
from pathlib import Path

import uvicorn
from fastapi.testclient import TestClient

from multiple_mcps_tools.server import create_app

app = create_app()

client = TestClient(app)

sales_path = Path("./data/sales.csv")
# sales_path = Path("./data/sales-complete.csv")

sales_data = sales_path.read_text(encoding="utf-8")

question = f"""
Rank the top 5 most sold products:

{sales_data}
"""

# Alternativa comentada equivalente ao seu código JS:
# question = f"""
# Here is a CSV file called sales.csv.
# What's the total revenue from this sales data?.
#
# {sales_data}
# """

try:
    response = client.post("/chat", json={"question": question})

    print(f"Response from /chat: {response.status_code}")
    print(response.text)
    sys.exit(0)

except Exception as error:
    print(f"Error testing /chat endpoint: {error}")
    sys.exit(1)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
