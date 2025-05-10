import asyncio
import base64
import os

import logfire
import nest_asyncio  # type: ignore
from agents import Agent, Runner, RunResultStreaming, set_default_openai_client
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()

nest_asyncio.apply()  # type: ignore

LANGFUSE_AUTH = base64.b64encode(
    f"{os.environ.get('LANGFUSE_PUBLIC_KEY')}:{os.environ.get('LANGFUSE_SECRET_KEY')}".encode()
).decode()

# Configure OpenTelemetry endpoint & headers
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = (
    os.environ.get("LANGFUSE_HOST") + "/api/public/otel"
)
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"

# Configure logfire instrumentation.
logfire.configure(
    service_name="my_agent_service",
    send_to_logfire=False,
)
# This method automatically patches the OpenAI Agents SDK to send logs via OTLP to Langfuse.
logfire.instrument_openai_agents()


async def main() -> None:
    openai_client = AsyncOpenAI()

    # Set the default OpenAI client for the Agents SDK
    # set trace off because of recomendation from OpenAI
    set_default_openai_client(openai_client, use_for_tracing=False)

    server = MCPServerStdio(
        name="weather server, via uv",
        params={
            "command": "uv",
            "args": ["run", "stdio_weather.py"],
        },
    )

    async with openai_client:
        async with server:
            await server.connect()

            agent = Agent(
                name="Assistant",
                instructions="You are a helpful assistant.",
                mcp_servers=[server],
                model="gpt-4.1-mini",
            )

            result: RunResultStreaming = Runner.run_streamed(
                agent, "東京に行きます。天気予報は？"
            )

            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(
                    event.data, ResponseTextDeltaEvent
                ):
                    print(event.data.delta, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
