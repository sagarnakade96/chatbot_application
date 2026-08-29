"""Superseded draft of the category nodes. Not imported anywhere. See
``nodes_file.py`` for the live versions.
"""

from langchain_aws import ChatBedrockConverse
from langgraph.graph import (
    StateGraph,
    START,
    END,
    add_messages,
)
from typing import Annotated, Literal

from pydantic import BaseModel, Field
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)
from typing_extensions import TypedDict
from state_file import ChatState

# NOTE: This module is an earlier draft. The graph in ``graph_build.py`` imports
# the terminal nodes from ``nodes_file.py`` instead, so nothing here is wired in.
# Kept for reference / history.

# Nodes

def hr_policy(state: ChatState):
    """Unused draft of the ``hr_policy`` terminal node.

    See :func:`nodes_file.hr_policy` for the version actually used by the graph.
    Re-emits ``state["prepared_response"]`` as an ``AIMessage``.
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
    """Unused draft of the ``product_information`` terminal node.

    See :func:`nodes_file.product_information` for the version used by the graph.
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
    """Unused draft of the ``product_complaint`` terminal node.

    See :func:`nodes_file.product_complaint` for the version used by the graph.
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


