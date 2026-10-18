from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from langgraph.graph.message import add_messages
from typing import Annotated
class State(BaseModel):
    """
    Represents the state of the agentic AI system and the structure of the state used in graph.
    """
    messages : Annotated[list, add_messages]