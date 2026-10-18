from  src.langgraph_agentic_ai.state.state import State
from langgraph.graph import START,END, StateGraph
from src.langgraph_agentic_ai.nodes.basic_chatbot_node import BasicChatbotNode

class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph.
        """
        self.basic_chatbot_node = BasicChatbotNode(self.llm) 
        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process_input)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot", END)
