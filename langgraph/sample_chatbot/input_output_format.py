"""I/O contracts for the bot: the ``Category`` type, the Pydantic models for
user input, the LLM's structured decision and the final output, plus the stdin
helper ``take_user_input``.
"""

from packages_file import Literal, BaseModel, Field

Category = Literal[
    "hr_policy",
    "product_information",
    "product_complaint"
]

class ChatInput(BaseModel):
    """Validated wrapper around a single raw user message.

    Using a model (instead of a bare ``str``) guarantees the message is
    non-empty before it ever reaches the graph.
    """

    message : str = Field(
        min_length=1,
        description="Message entered by the user"
    )

class RoutingDecision(BaseModel):
    """Schema the LLM is forced to fill in via ``with_structured_output``.

    One call to the model yields the routing category, a human-readable reason
    for the choice, and a ready-to-send answer for the user.
    """

    category:Category = Field(
        description="Category selected for the user's request."
    )
    reason: str = Field(
        description= "Short explanation of why this category was selected."
    )
    response:str = Field(
        description= "Helpful response that should be returned to the user."
    )


def take_user_input() -> ChatInput:
    """Prompt for one line on stdin and return it as a validated ``ChatInput``.

    Raises:
        pydantic.ValidationError: if the user submits an empty line.

    Returns:
        A ``ChatInput`` holding the stripped message text.
    """

    message = input(
        "\nYou: "
    ).strip()

    return ChatInput(
        message=message
    )
class ChatOutput(BaseModel):
    """Final result shown to the user after one graph run.

    Built by the runner from the compiled graph's output state: ``category``
    comes from ``decision`` and ``response`` from the last message's content.
    """

    category: Category
    response: str