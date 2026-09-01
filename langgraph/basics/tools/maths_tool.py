from langchain_core.tools import tool

@tool
def add(a:int,b:int)-> int:
    """This function does addition of a : int variable and b : int variable

    Args:
        a (int): integer variable
        b (int): integer variable

    Returns:
        int: addition of a and b integer value
    """
    return a + b