"""Assembles the LangGraph state machine.

Registers nodes, wires the START -> prepare_input -> invoke_llm edges, adds the
conditional edge that routes on the LLM's category, and compiles the graph into
the module-level ``app``. Importing this module builds and compiles the graph.
"""

from state_file import ChatState
from packages_file import StateGraph, START,END
from nodes_file import prepare_input, hr_policy, product_information, product_complaint
from llm_file import invoke_llm
from routers import route_request
builder = StateGraph(ChatState)

builder.add_node("prepare_input",prepare_input)
builder.add_node("invoke_llm", invoke_llm)
builder.add_node("hr_policy", hr_policy)
builder.add_node("product_information", product_information)
builder.add_node("product_complaint", product_complaint)


# Start edges
builder.add_edge(START, "prepare_input")
builder.add_edge("prepare_input", "invoke_llm")

builder.add_conditional_edges(
    "invoke_llm",
    route_request,
    {
        "hr_policy": "hr_policy",
        "product_information": "product_information",
        "product_complaint": "product_complaint",
    }
)

#End Edges

builder.add_edge(
    "hr_policy",
    END,
)

builder.add_edge(
    "product_information",
    END,
)

builder.add_edge(
    "product_complaint",
    END,
)

app = builder.compile()


def draw_graph():
    """Print the compiled graph as Mermaid text and save a PNG rendering.

    Writes ``customer_support_graph.png`` next to this module. Rendering the PNG
    requires network access (LangGraph calls the mermaid.ink service). Call this
    once for documentation; it is not needed to run the bot.
    """

    print("\n--- Mermaid Graph ---")

    mermaid_code = app.get_graph().draw_mermaid()

    print(mermaid_code)

    app.get_graph().draw_mermaid_png(
        output_file_path="customer_support_graph.png"
    )

    print(
        "\nGraph saved as customer_support_graph.png"
    )