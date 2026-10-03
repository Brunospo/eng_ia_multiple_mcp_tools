import os


def get_fs_tool():
    return {
        "filesystem": {
            "transport": "stdio",
            "command": "npx",
            "args": [
                "-y",
                "@modelcontextprotocol/server-filesystem",
                os.path.join(os.getcwd(), "reports"),
            ],
        }
    }
