from pydantic import BaseModel, Field
from typing import Annotated, Literal
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
from dataclasses import dataclass
import random

# States


# With dataclass defining the states
@dataclass
class ChatState:
    name : str
    game : Literal["Cricket", "Badminton"] | None = None

# With Pydantic defining the states
# class ChatState(BaseModel):
#     name : str
#     game : Literal["Cricket", "Badminton"] | None = None

def print_status(state_name:str)-> str:
    print(f"-"*50)
    print(f"{state_name} Node Has Been Called")
    print(f"-"*50)
    print("↓\n"*2)

# Nodes
def play_game(state: ChatState):
    print_status(state_name="Play Game")
    data = {
        "name":state.name + " Want to play"
    }
    return data

def play_cricket(state:ChatState):
    print_status(state_name="Play Cricket")
    data = {
        "name":state.name + " Cricket","game":"Cricket"
    }
    return data

def play_badminton(state:ChatState):
    print_status(state_name="Play Badminton")
    data = {
         "name":state.name + " Badminton","game":"Badminton"
    }
    return data

def decide_play(state:ChatState)->Literal["play_cricket", "play_badminton"]:
    if random.random() < 0.5:
        return "play_cricket"
    return "play_badminton"


def draw_graph(graph):
    print("\n--- Mermaid Graph ---")
    mermaid_code = graph.get_graph()
    print(mermaid_code)
    graph.get_graph().draw_mermaid_png(
        output_file_path="game_choice_flow.png"
    )

# Builder

builder = StateGraph(ChatState)
builder.add_node("play_game", play_game)
builder.add_node("play_cricket",play_cricket)
builder.add_node("play_badminton",play_badminton)

# Edges
builder.add_edge(START, "play_game")
builder.add_conditional_edges("play_game",decide_play)
builder.add_edge("play_cricket", END)
builder.add_edge("play_badminton", END)

# Graph
graph = builder.compile()

# Display Graph
# draw_graph(graph=graph)

# invoke Graph
result = graph.invoke({"name":"Sagar"})
print(result)