from functools import lru_cache
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from langchain_core.messages import AIMessage, HumanMessage
from pydantic import BaseModel, Field

from src.langgraph_agentic_ai.graph.graph_builder import GraphBuilder
from src.langgraph_agentic_ai.LLMS.claude_model import model

router = APIRouter(prefix="/basic-chatbot", tags=["basic_chatbot"])


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    history: list[ChatMessage] = Field(
        default_factory=list,
        description=(
            "Prior turns, oldest first. The graph has no checkpointer, so "
            "there is no server-side memory between calls."
        ),
    )


class ChatResponse(BaseModel):
    reply: str


@lru_cache
def get_compiled_graph():
    """Builds and compiles the basic_chatbot graph once per process.

    Reuses GraphBuilder / the node / the model exactly as implemented in
    src/langgraph_agentic_ai -- nothing there is duplicated or reimplemented.
    Override via app.dependency_overrides[get_compiled_graph] in tests.
    """
    builder = GraphBuilder(model)
    builder.basic_chatbot_build_graph()
    return builder.graph_builder.compile()


@router.post("/chat", response_model=ChatResponse)
def chat(body: ChatRequest, graph=Depends(get_compiled_graph)) -> ChatResponse:
    messages = [
        (HumanMessage if turn.role == "user" else AIMessage)(content=turn.content)
        for turn in body.history
    ]
    messages.append(HumanMessage(content=body.message))

    try:
        result = graph.invoke({"messages": messages})
    except Exception as exc:  # Bedrock/boto/graph errors
        raise HTTPException(
            status_code=502, detail=f"Chat graph invocation failed: {exc}"
        ) from exc

    return ChatResponse(reply=result["messages"][-1].content)
