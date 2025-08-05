from fastapi import APIRouter, HTTPException
from app.agents.assistant_agent import handle_assistant_message
from app.models.schemas import AssistantMessageRequest

router = APIRouter()

@router.post("/message")
async def assistant_message(request: AssistantMessageRequest):
    try:
        return handle_assistant_message(request.message, request.action_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))