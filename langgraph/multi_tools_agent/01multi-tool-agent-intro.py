import os
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from llm_file import llm
from dotenv import load_dotenv
load_dotenv()

# arxiv wrapper tool
# api_wrapper_arxiv = ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=200)

# arxiv = ArxivQueryRun(api_wrapper=api_wrapper_arxiv)

# response = arxiv.invoke(
#     "Memory management for AI agents"
# )

# print(response)
# Above is the arxiv tool, but it is not working properly, so I am using the wikipedia tool below. reason : tools are being deprecated in langchain_community, so I am using the wikipedia tool below.

api_wrapper_wikipedia = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=200)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper_wikipedia)

wiki.invoke("Who is Elon Musk?")



os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

tavily = TavilySearchResults()

tavily.invoke("Provide me the recent AI news for the month august 2026")

# print(response)


# Combine All Tools

tools = [wiki, tavily]


# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)

response = llm_with_tools.invoke([
    HumanMessage(
        content="What is the recent AI news for the month of August 2026?"
    )
]).tool_calls
