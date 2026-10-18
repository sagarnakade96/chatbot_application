from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_classic.tools.retriever import create_retriever_tool

from dotenv import load_dotenv
load_dotenv() 
urls=[
    "https://langchain-ai.github.io/langgraph/tutorials/introduction/",
    "https://langchain-ai.github.io/langgraph/tutorials/workflows/",
    "https://langchain-ai.github.io/langgraph/how-tos/map-reduce/"
]

doc_loader=[]
for url in urls:
    loader = WebBaseLoader(url)
    doc_loader.append(loader)

print(doc_loader)

doc_list = []
for loader in doc_loadfer:
    doc = loader.load()
    doc_list.extend(doc)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs_splits = text_splitter.split_documents(doc_list)

vectore_store_langchain = FAISS.from_documents(documents=docs_splits, embedding=OpenAIEmbeddings())

retriever_langchain = vectore_store_langchain.as_retriever()

# retriever_langchain.invoke("Tell me about LangGraph and its features.")

retriever_tool_langchain = create_retriever_tool(
retriever_langchain,
)