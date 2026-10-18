from fastapi import APIRouter

from app.api.v1 import health
from app.apps.basic_chatbot.router import router as basic_chatbot_router

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(basic_chatbot_router)

# Register each app's router here, e.g.:
#   from app.apps.<name>.router import router as <name>_router
#   api_router.include_router(<name>_router)
