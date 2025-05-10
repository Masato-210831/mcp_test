from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")


@mcp.tool()
async def get_mcp_server_info() -> str:
    """Get information about the MCP server."""
    return "streamable-http MCP server is running"


@mcp.tool()
async def get_alerts(prefecture: str) -> str:
    """Get weather alerts for a Japan prefecture.

    Args:
        prefecture: Japan prefecture name (e.g. Tokyo, Osaka)
    """
    print(prefecture)

    return "現在警報はありません"


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """

    return "東京は雨です"


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="streamable-http")

    #  npx @modelcontextprotocol/inspector で確認
