def get_mongodb_tool():
    return {
        "MongoDB": {
            "transport": "stdio",
            "command": "npx",
            "args": ["-y", "mongodb-mcp-server@latest"],
            "env": {
                "MDB_MCP_CONNECTION_STRING": "mongodb://localhost:27017/dataprocessing"
            },
        }
    }
