import asyncio
from typing import Any

from dotenv import load_dotenv
from langchain_mcp_adapters.tools import load_mcp_tools  # type: ignore
from langfuse.callback import CallbackHandler  # type: ignore
from langgraph.prebuilt import create_react_agent  # type: ignore
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

langfuse_handler = CallbackHandler()

server_params = StdioServerParameters(command="python", args=["stdio_weather.py"])


async def main() -> None:
    async with stdio_client(server=server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # MCPサーバーとのハンドシェイク
            await session.initialize()

            # MCPサーバーのツールを読み込む
            tools: Any = await load_mcp_tools(session)

            # エージェントを作成
            agent: Any = create_react_agent("openai:gpt-4.1-mini", tools)

            agent_respose = await agent.ainvoke(
                {"messages": [("user", "東京の明日の天気を知りたい")]},
                config={"callbacks": [langfuse_handler]},
            )

            print(agent_respose["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
