import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("local-file-server")

DIRECTORY = "/Users/masato/Desktop/obsidian_vault"

# ファイルを読むリソース


@mcp.resource("file://{filename}/")
def read_file(filename: str) -> str:
    filepath = os.path.join(DIRECTORY, filename)
    print(filepath)

    file_path = Path(filepath)

    if file_path.glob("xn--*.md"):
        decoded = file_path.stem.encode("ascii").decode("idna")
        decoded = decoded[0].upper() + decoded[1:] + ".md"
        filepath = os.path.join(DIRECTORY, decoded)

        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    if not os.path.isfile(filepath):
        return f"File({filepath}) not found."

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


# ファイル一覧を出すリソース


@mcp.resource("files://list")
def list_files() -> str:
    files: list[str] = []

    for filename in os.listdir(DIRECTORY):
        filepath = os.path.join(DIRECTORY, filename)

        if os.path.isfile(filepath):
            files.append(filename)

    return "\n".join(files)


# サンプルテキストを返すリソース


@mcp.resource("test://sample")
def sample_text() -> str:
    return "これはサンプルテキストです。MCPが正常に動作しています。"


if __name__ == "__main__":
    print("Starting MCP server...")

    mcp.run()
