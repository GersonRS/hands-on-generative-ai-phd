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
        base_url="https://llm-server-compass.luizalabs.com/v1",
        api_key="eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJURGV3MjJQZ3VYY1J1LWY1UDFhZnFma211TVJhZWF2VU5hc1N4NVpRelcwIn0.eyJleHAiOjE3ODI0NTcxOTgsImlhdCI6MTc1MDkyMTE5OCwiYXV0aF90aW1lIjoxNzUwOTE5NzMxLCJqdGkiOiJmMjY1NWRmNC1jYTYxLTQxMDQtODE4ZC02M2QzMjcwNzQ3MmYiLCJpc3MiOiJodHRwczovL3Nzby1jb3JwLmx1aXphbGFicy5jb20vcmVhbG1zL2NvcnAiLCJzdWIiOiJmOmRkMmJmZWNjLWQxN2ItNGUzMi05MTM4LWFiNWY1OTcxNDViYzpTQU5UT1MuR0VSU09OIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiY29tcGFzc19hcGkiLCJzaWQiOiIxMDRkYzQ0MS1mNzI1LTQ3N2ItOGE4ZC0yOTI3ZTZjYjRlMDQiLCJhY3IiOiIwIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIl19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIG9mZmxpbmVfYWNjZXNzIGVtYWlsIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJuYW1lIjoiR2Vyc29uIFJvZHJpZ3VlcyBTYW50b3MiLCJyZWdpc3RyYXRpb25faWQiOjM3ODk3NCwicHJlZmVycmVkX3VzZXJuYW1lIjoic2FudG9zLmdlcnNvbiIsImxvY2FsZSI6InB0LUJSIiwibG9naW4iOiJzYW50b3MuZ2Vyc29uIiwiZ2l2ZW5fbmFtZSI6IkdlcnNvbiIsImZhbWlseV9uYW1lIjoiU2FudG9zIiwiYnJhbmNoIjo3MDAzLCJlbWFpbCI6InNhbnRvcy5nZXJzb25AbHVpemFsYWJzLmNvbSIsInZhbGlkX2VtYWlsIjoic2FudG9zLmdlcnNvbkBsdWl6YWxhYnMuY29tIn0.2S-rq2WIhPy225I8_A5zC-mIycbRtbl00eYhkPVqSN3u_XLJW-HNfslc3DTANa4iJ-zVJhWsroE-LljR-eJw30syWDgrDk2DnSJAxala-lrFR02sXQWyEKVk7v-wKBX_zaRAq4O9h-CPz-_huExOrEiYdsq7ZsHIFHcygIZJDquHRtC4p_TpOlb2r0pku7bvVTfRKLDjB54Y2sVmw4Z4Vij7_02eGeP69746y4ixgigucXmzqZvUPjBhzE60_gpC9hDKpVErAOkFy3gxfV2IJEVFamwloWMkPfbuEjUM20LAV3YAYRb09eRh2d5r70wSf-Kv7bJrhJ1Ey_MRlj4fXQ",
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
