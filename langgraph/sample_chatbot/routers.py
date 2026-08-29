"""Routing function for the conditional edge after ``invoke_llm``."""

from state_file import ChatState
from input_output_format import Category

def route_request(state: ChatState) -> Category:
    """Routing function for the conditional edge after ``invoke_llm``.

    LangGraph calls this with the current state and uses the returned string to
    select the next node via the mapping registered in
    ``builder.add_conditional_edges`` (see ``graph_build.py``).

    Args:
        state: The current graph state. Reads ``decision``.

    Returns:
        The category chosen by the LLM (one of ``"hr_policy"``,
        ``"product_information"``, ``"product_complaint"``), which is also the
        name of the node to run next.
    """

    print("\n[route_request]")

    print(
        f"Routing to: {state['decision']}"
    )

    return state["decision"]

