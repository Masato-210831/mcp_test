import json

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")


@mcp.tool()
async def get_mcp_server_info() -> str:
    """Get information about the MCP server."""
    return "stdio MCP server is running"


@mcp.tool()
async def get_alerts(prefecture: str) -> str:
    """Get weather alerts for a Japan prefecture.

    Args:
        prefecture: Japan prefecture name (e.g. Tokyo, Osaka)
    """
    print(prefecture)

    return "現在警報はありません"


@mcp.tool()
async def get_weather(location: str) -> str:
    """Get current temperature and weather for a given location in English.

    Args:
        location: City e.g. San Francisco, Tokyo
    """

    lower_location: str = location.lower()

    match lower_location:
        case "tokyo":
            return json.dumps(
                {"location": "Tokyo", "temperature": "10", "weather": "sunny"}
            )
        case "san francisco":
            return json.dumps(
                {"location": "San Francisco", "temperature": "72", "weather": "cloudy"}
            )
        case "paris":
            return json.dumps(
                {"location": "Paris", "temperature": "22", "weather": "rainy"}
            )
        case _:
            return json.dumps(
                {"location": location, "temperature": "unknown", "weather": "unknown"}
            )


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")

    #  npx @modelcontextprotocol/inspector で確認
