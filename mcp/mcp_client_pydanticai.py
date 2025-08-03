import asyncio
import json

from httpx import AsyncClient
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

data = {
    "ambiente": "oi",
    "org": "magazineluiza",
    "squad": "chapter-mle",
    "tribe": "data-science",
    "vertical": "MLE",
}
tags = json.dumps(data)
headers = {"tags": tags}
custom_http_client = AsyncClient(headers=headers)

model = OpenAIModel(
    "gemini-2.5-pro",
    provider=OpenAIProvider(
        http_client=custom_http_client,
    ),
)
server = MCPServerHTTP(url="http://localhost:8000/sse")  # legacy
server_b = MCPServerHTTP(url="http://localhost:9000/sse")  # legacy
agent = Agent(model, mcp_servers=[server, server_b])


prompt = """
Qual preço do item de ID 1?
"""


async def main():
    async with agent.run_mcp_servers():
        result = await agent.run(prompt)
    print(result.output)


asyncio.run(main())
