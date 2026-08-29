"""Graph nodes: ``prepare_input`` (entry) and the three category terminal nodes.

These are the nodes actually registered in ``graph_build.py`` (unlike the drafts
in ``decision_nodes.py``).
"""

from state_file import ChatState
from packages_file import HumanMessage, AIMessage

def prepare_input(state: ChatState):
    """Entry node of the graph.

    Takes the plain string in ``state["raw_input"]`` (set by the runner when
    ``app.invoke`` is called) and wraps it in a LangChain ``HumanMessage``.

    Args:
        state: The current graph state. Only ``raw_input`` is read.

    Returns:
        A partial state update ``{"messages": [HumanMessage(...)]}``. Because the
        ``messages`` channel uses the ``add_messages`` reducer, this new message
        is appended to the running conversation history rather than replacing it.
    """

    print("\n[prepare_input]")
    print("Preparing user's message...")

    user_message = HumanMessage(
        content=state["raw_input"]
    )

    print(
        f"User Message Received : {user_message}"
    )

    return {
        "messages": [user_message]
    }


# policy  nodes
def hr_policy(state:ChatState):
    """Terminal node for the ``hr_policy`` category.

    The actual answer text was already produced by the LLM in ``invoke_llm`` and
    stored in ``state["prepared_response"]``. This node simply emits it as an
    ``AIMessage`` so it becomes the last message in the conversation. In a real
    system this is where you would enrich the reply with HR-specific data
    (leave balances, policy documents, etc.).

    Args:
        state: The current graph state. Reads ``prepared_response``.

    Returns:
        A partial state update appending one ``AIMessage`` to ``messages``.
    """
    print("\n[hr_policy]")
    print(
        "This user is interested in HR policies."
    )

    return {
        "messages": [
            AIMessage(
                content=state["prepared_response"]
            )
        ]
    }


def product_information(state: ChatState):
    """Terminal node for the ``product_information`` category.

    Mirrors :func:`hr_policy`: it re-emits the LLM-prepared answer stored in
    ``state["prepared_response"]`` as an ``AIMessage``. Extend this node to look
    up live catalogue data, pricing or specifications.

    Args:
        state: The current graph state. Reads ``prepared_response``.

    Returns:
        A partial state update appending one ``AIMessage`` to ``messages``.
    """

    print("\n[product_information]")
    print(
        "This user is interested in product information."
    )

    return {
        "messages": [
            AIMessage(
                content=state["prepared_response"]
            )
        ]
    }


def product_complaint(state: ChatState):
    """Terminal node for the ``product_complaint`` category.

    Mirrors :func:`hr_policy`: it re-emits the LLM-prepared answer stored in
    ``state["prepared_response"]`` as an ``AIMessage``. Extend this node to open
    a support ticket, start a return/refund flow, etc.

    Args:
        state: The current graph state. Reads ``prepared_response``.

    Returns:
        A partial state update appending one ``AIMessage`` to ``messages``.
    """

    print("\n[product_complaint]")
    print(
        "This user has a product complaint."
    )

    return {
        "messages": [
            AIMessage(
                content=state["prepared_response"]
            )
        ]
    }