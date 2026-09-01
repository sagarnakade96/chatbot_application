from llm_file import llm
from tools.maths_tool import add
from pydantic import BaseModel
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.graph import add_messages, StateGraph, START,END
from typing import Annotated
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from pprint import pprint

init_message = {
    "messages": [
        HumanMessage(
            content="Tell me what is AI, define in 2 lines?"
        )
    ]
}

tools = [add]

def draw_graph(graph):
    print("\n--- Mermaid Graph ---")
    mermaid_code = graph.get_graph()
    print(mermaid_code)
    graph.get_graph().draw_mermaid_png(
        output_file_path="01tool_calling.png"
    )

class StateClass(BaseModel):
    messages : Annotated[list[AnyMessage], add_messages]


def tool_call(state:StateClass):
    llm_with_tool = llm.bind_tools([add])
    response = llm_with_tool.invoke(state.messages)
    return {
        "messages": [response]
    }

# graph
builder = StateGraph(StateClass)

builder.add_node("llm_tool", tool_call)
builder.add_node("tools", ToolNode(tools=tools))

builder.add_edge(START, "llm_tool")
builder.add_conditional_edges(
    "llm_tool",
    tools_condition
)


builder.add_edge("tools", END)

graph = builder.compile()


# draw_graph(graph=graph)

result = graph.invoke(init_message)

for message in result["messages"]:
    message.pretty_print()