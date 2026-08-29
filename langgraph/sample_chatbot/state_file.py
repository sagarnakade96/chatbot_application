"""Definition of ``ChatState``, the typed dict LangGraph threads through nodes."""

from packages_file import TypedDict, AnyMessage, add_messages, Annotated
from input_output_format import Category

class ChatState(TypedDict, total=False):
    """Shared state passed between every node in the graph.

    ``total=False`` means all keys are optional, so each node only has to return
    the keys it actually produces. LangGraph merges those partial updates into
    the running state.

    Keys:
        raw_input: The plain user string, set by the runner in ``app.invoke``.
        messages: The conversation history. The ``add_messages`` reducer makes
            node returns *append* to this list instead of overwriting it.
        decision: Category chosen by the LLM; drives conditional routing.
        decision_reason: Why the LLM picked that category (logging only).
        prepared_response: The answer text drafted by the LLM, re-emitted as an
            ``AIMessage`` by whichever terminal node runs.
    """

    raw_input: str
    messages: Annotated[
        list[AnyMessage],
        add_messages,
    ]
    decision: Category
    decision_reason: str
    prepared_response: str

