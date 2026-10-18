from fastapi import APIRouter

router = APIRouter(prefix="/basic-chatbot", tags=["basic_chatbot"])


@router.get("")
def index() -> dict[str, str]:
    """Placeholder route; real functionality not implemented yet."""
    return {"app": "basic_chatbot", "status": "not implemented"}
