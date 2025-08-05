from pydantic import BaseModel
from typing import Optional, Dict, Any

class DevStyleResponse(BaseModel):
    text: str                   # HTML-formatted response
    data: Optional[Dict] = None # Raw JSON data
    success: bool

class AssistantMessageRequest(BaseModel):
    message: str
    action_type: Optional[str] = None