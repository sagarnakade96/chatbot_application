from package_file import tool

@tool
def attach_name(name : str = "Sagar")-> str:
    """This function takes a name as input and returns a welcome message for the story session.
    """
    return f"Hello {name}!, Welcome to the story session. Let's start the story with your topic and see how it unfolds."