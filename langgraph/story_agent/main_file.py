from llm_file import llm
from package_file import display,Image,TypedDict, BaseModel, Field, Annotated, Literal, ChatBedrockConverse, StateGraph, START, END, add_messages, AnyMessage, HumanMessage, AIMessage, SystemMessage
from nodes import generate_a_story, resolve_conflicted_story, improved_story, polished_story


class BaseState(TypedDict):
    """Base state for the story agent."""
    topic: str
    story: str
    improvised_story: str
    final_story: str

graph = StateGraph(BaseState)

# Add nodes to the graph
graph.add_node("generate", generate_a_story)
graph.add_node("improve", improved_story)
graph.add_node("polish", polished_story)

# Add edges to the graph
graph.add_edge(START, "generate")
graph.add_conditional_edges("generate", resolve_conflicted_story, {"Pass": "improve", "Fail": "generate"})
graph.add_edge("improve", "polish")
graph.add_edge("polish", END)

compiled_graph = graph.compile()

# display image
# graph_image = compiled_graph.get_graph().draw_mermaid_png(output_file_path="story_agent_graph.png")
# display(Image(graph_image))



result = compiled_graph.invoke(input={"topic": "A brave knight", "story": "Once upon a time, there was a brave knight who fought dragons.", "improvised_story": "", "final_story": ""})
print(result)
print("-"*100)
print(result.get("story", [])[0].content)
print("-"*100)
print(result.get("final_story", [])[0].content)
