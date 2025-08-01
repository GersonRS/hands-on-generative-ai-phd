import asyncio
import os

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

model = ChatOpenAI(model="gpt-3.5-turbo")

system_message = "You are a helpful assistant. Respond only in Portuguese."

client = MultiServerMCPClient(
    {
        "math": {"transport": "streamable_http", "url": "http://localhost:8000/mcp"},
        "itens": {"transport": "streamable_http", "url": "http://localhost:9000/mcp"},
    }
)


async def main():
    tools = await client.get_tools()
    agent = create_react_agent(model, tools, prompt=system_message)
    response = await agent.ainvoke(
        {
            "messages": "Multiplique 5 vezes 6 depois some mais 2, o resultado é o preço da laranja, com esse valor salve o Item Laranja. Crie um plano antes de executar a tarefa."
        }
    )
    print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())


# questions
# what's (3 + 5) x 12?
# Multiplique 2x10 o resultado é o preço da laranja, com esse valor salve o Item laranja
# Cadastre o item laranja e o preço dele é 2 vezes 10
