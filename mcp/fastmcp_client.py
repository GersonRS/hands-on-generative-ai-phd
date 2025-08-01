import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")  # Assumes my_mcp_server.py exists


async def main():
    # Connection is established here
    async with client:
        print(f"Client connected: {client.is_connected()}")

        # Make MCP calls within the context
        tools = await client.list_tools()
        print(f"\nAvailable tools: {tools} \n")

        if any(tool.name == "function_name" for tool in tools):
            result = await client.call_tool(
                "function_name", {"name": "Lapis"}
            )
            print(f"Greet result: {result}")

    # Connection is closed automatically here
    print(f"\n Client connected: {client.is_connected()}")


if __name__ == "__main__":
    asyncio.run(main())
