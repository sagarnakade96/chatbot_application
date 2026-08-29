"""LLM setup and the ``invoke_llm`` node.

Creates the Bedrock chat model, wraps it with ``with_structured_output`` so it
must return a ``RoutingDecision``, and exposes the node that classifies the
user's message and drafts a reply.
"""

# files import
from input_output_format import RoutingDecision
from packages_file import ChatBedrockConverse, SystemMessage
from state_file import ChatState
from prompts import SYSTEM_PROMPT

llm = ChatBedrockConverse(
        credentials_profile_name="develop-admin",
        model = "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        region_name="us-east-1",
        temperature=0.1,
        max_tokens=1000,
    )
routing_llm = llm.with_structured_output(
    RoutingDecision
)

def invoke_llm(state:ChatState):
    """Core reasoning node: classify the user's message and draft a reply.

    Prepends the classifier ``SYSTEM_PROMPT`` to the running message history and
    calls the structured-output LLM (``routing_llm``), which is forced to return
    a :class:`RoutingDecision` (category + reason + response).

    Args:
        state: The current graph state. Reads ``messages``.

    Returns:
        A partial state update with three keys consumed downstream:
        ``decision`` (the category, used by :func:`route_request` to pick the
        next node), ``decision_reason`` (for logging/debugging) and
        ``prepared_response`` (the answer text re-emitted by the terminal node).
    """
    print("\n[invoke_llm]")
    print("Sending request to AWS Bedrock...")

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"],
    ]

    decision: RoutingDecision = routing_llm.invoke(
        messages
    )

    print(
        f"LLM decision: {decision.category}"
    )

    print(
        f"Reason: {decision.reason}"
    )

    return {
        "decision": decision.category,
        "decision_reason": decision.reason,
        "prepared_response": decision.response,
    }