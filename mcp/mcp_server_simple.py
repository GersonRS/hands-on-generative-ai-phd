from mcp.server.fastmcp import FastMCP

server = FastMCP("StatelessServer", stateless_http=True, json_response=True)


@server.tool()
async def sum_number(a: int, b: int) -> str:
    print(f"\nSum -- {a+b}\n")
    return str(a + b)


@server.tool()
async def multiply_number(a: int, b: int) -> str:
    print(f"\nMultiply -- {a*b}\n")
    return str(a * b)


if __name__ == "__main__":
    # server.run(transport="sse")
    server.run(transport="streamable-http")
