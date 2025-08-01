import asyncio

from fastapi import FastAPI, HTTPException
from fastmcp import FastMCP
from pydantic import BaseModel


# Define your Pydantic model
class Item(BaseModel):
    name: str
    price: float


# Create your FastAPI app
app = FastAPI()
items = {}  # In-memory database


@app.get("/items")
def list_items():
    """List all items"""
    return list(items.values())


@app.get("/items/{item_id}")
def get_item(item_id: int):
    """Get item by ID"""
    if item_id not in items:
        raise HTTPException(404, "Item not found")
    return items[item_id]


@app.post("/items")
def create_item(item: Item):
    """Create a new item"""
    item_id = len(items) + 1
    items[item_id] = {"id": item_id, **item.model_dump()}
    print(f"\n Item --> {items}")
    return items[item_id]


@app.post("/get_item_price")
def get_item_price_by_id(item_id: int):
    """Create a new item"""
    print(f"\n Item --> {item_id}")
    return items[item_id]


# Test your MCP server with a client
async def check_mcp(mcp: FastMCP):
    # List the components that were created
    tools = await mcp.get_tools()
    resources = await mcp.get_resources()
    templates = await mcp.get_resource_templates()

    print(f"{len(tools)} Tool(s): {', '.join([t.name for t in tools.values()])}")
    print(f"{len(resources)} Resource(s): {', '.join([r.name for r in resources.values()])}")
    print(
        f"{len(templates)} Resource Template(s): {', '.join([t.name for t in templates.values()])}"
    )

    return mcp


if __name__ == "__main__":
    # Create MCP server from FastAPI app
    mcp = FastMCP.from_fastapi(app=app)

    asyncio.run(check_mcp(mcp))
    # mcp.run(transport="sse", port=9000)
    # In a real scenario, you would run the server:
    mcp.run(transport="streamable-http", host="127.0.0.1", port=9000, path="/mcp")
