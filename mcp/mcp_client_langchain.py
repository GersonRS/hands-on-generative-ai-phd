import asyncio
import json
import os

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.streamable_http import streamablehttp_client

os.environ["OPENAI_API_KEY"] = (
    "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJURGV3MjJQZ3VYY1J1LWY1UDFhZnFma211TVJhZWF2VU5hc1N4NVpRelcwIn0.eyJleHAiOjE3ODI0NTcxOTgsImlhdCI6MTc1MDkyMTE5OCwiYXV0aF90aW1lIjoxNzUwOTE5NzMxLCJqdGkiOiJmMjY1NWRmNC1jYTYxLTQxMDQtODE4ZC02M2QzMjcwNzQ3MmYiLCJpc3MiOiJodHRwczovL3Nzby1jb3JwLmx1aXphbGFicy5jb20vcmVhbG1zL2NvcnAiLCJzdWIiOiJmOmRkMmJmZWNjLWQxN2ItNGUzMi05MTM4LWFiNWY1OTcxNDViYzpTQU5UT1MuR0VSU09OIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiY29tcGFzc19hcGkiLCJzaWQiOiIxMDRkYzQ0MS1mNzI1LTQ3N2ItOGE4ZC0yOTI3ZTZjYjRlMDQiLCJhY3IiOiIwIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIl19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIG9mZmxpbmVfYWNjZXNzIGVtYWlsIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJuYW1lIjoiR2Vyc29uIFJvZHJpZ3VlcyBTYW50b3MiLCJyZWdpc3RyYXRpb25faWQiOjM3ODk3NCwicHJlZmVycmVkX3VzZXJuYW1lIjoic2FudG9zLmdlcnNvbiIsImxvY2FsZSI6InB0LUJSIiwibG9naW4iOiJzYW50b3MuZ2Vyc29uIiwiZ2l2ZW5fbmFtZSI6IkdlcnNvbiIsImZhbWlseV9uYW1lIjoiU2FudG9zIiwiYnJhbmNoIjo3MDAzLCJlbWFpbCI6InNhbnRvcy5nZXJzb25AbHVpemFsYWJzLmNvbSIsInZhbGlkX2VtYWlsIjoic2FudG9zLmdlcnNvbkBsdWl6YWxhYnMuY29tIn0.2S-rq2WIhPy225I8_A5zC-mIycbRtbl00eYhkPVqSN3u_XLJW-HNfslc3DTANa4iJ-zVJhWsroE-LljR-eJw30syWDgrDk2DnSJAxala-lrFR02sXQWyEKVk7v-wKBX_zaRAq4O9h-CPz-_huExOrEiYdsq7ZsHIFHcygIZJDquHRtC4p_TpOlb2r0pku7bvVTfRKLDjB54Y2sVmw4Z4Vij7_02eGeP69746y4ixgigucXmzqZvUPjBhzE60_gpC9hDKpVErAOkFy3gxfV2IJEVFamwloWMkPfbuEjUM20LAV3YAYRb09eRh2d5r70wSf-Kv7bJrhJ1Ey_MRlj4fXQ"  # can be anything
)
os.environ["OPENAI_API_BASE"] = "https://llm-server-compass.luizalabs.com/v1"
data = {
    "ambiente": "oi",
    "org": "magazineluiza",
    "squad": "chapter-mle",
    "tribe": "data-science",
    "vertical": "MLE",
}
tags = json.dumps(data)

model = ChatOpenAI(model="gemini-2.5-pro", default_headers={"tags": tags})

system_message = "You are a helpful assistant. Respond only in Portuguese."


async def main():
    async with streamablehttp_client("http://127.0.0.1:8000/mcp") as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(model, tools, prompt=system_message)
            agent_response = await agent.ainvoke({"messages": "Eu quero um poema sobre flores"})
            print(agent_response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
