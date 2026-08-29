"""Entry point. Run ``python runner.py`` to start the interactive chatbot."""

from packages_file import AnyMessage
from input_output_format import take_user_input, ChatOutput
from graph_build import app, draw_graph

def run_chatbot():
    """Interactive REPL loop that drives the compiled graph.

    Reads a message, invokes the graph once per turn, and prints the routed
    category plus the bot's reply. Conversation history is threaded back into
    each ``app.invoke`` call so the graph sees the full dialogue. Type ``exit``
    to quit.
    """

    history: list[AnyMessage] = []

    print("\nCustomer Support Bot")
    print("Type 'exit' to stop.")

    while True:

        user_input = take_user_input()

        if user_input.message.lower() == "exit":
            print("Bot: Goodbye!")
            break

        result = app.invoke(
            {
                "raw_input": user_input.message,
                "messages": history,
            }
        )

        # Save the updated conversation.
        history = result["messages"]

        output = ChatOutput(
            category=result["decision"],
            response=result["messages"][-1].content,
        )

        print(
            f"\nCategory: {output.category}"
        )

        print(
            f"Bot: {output.response}"
        )


if __name__ == "__main__":

    # First create/display graph.
    # draw_graph()

    # Only after drawing it do we invoke the bot.
    run_chatbot()