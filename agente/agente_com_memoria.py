from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI

# Inicialização da ferramenta de busca
search = DuckDuckGoSearchRun()
tools = [
    Tool(name="Search", func=search.run, description="Busca na web"),
]

# Memória de conversação
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Instância do modelo (usa OPENAI_API_KEY via variável de ambiente)
llm = ChatOpenAI()

# Criação do agente com tratamento de erro de parsing
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    handle_parsing_errors=True,  # <- aqui está o tratamento do erro
    verbose=True,  # <- opcional, para debug detalhado
)

# Executar uma pergunta
pergunta = "Quem é o presidente do Brasil?"
resposta = agent.invoke(pergunta)

print(f"Pergunta: {pergunta}")
print("Resposta do agente:", resposta)
