from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Qdrant
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# 1. Carregar documentos
loader = TextLoader("rag/documents/exemplo.txt")
docs = loader.load()

# 2. Quebrar em pedaços
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# 3. Gerar embeddings e armazenar

# # 3. Gerar embeddings e armazenar
embeddings = OpenAIEmbeddings()
qdrant = Qdrant.from_documents(chunks, embeddings, location=":memory:", collection_name="meus_docs")

# # 4. Criar pipeline RAG
qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(), retriever=qdrant.as_retriever())
resposta = qa.run("Quem é Gerson?")
print(resposta)
