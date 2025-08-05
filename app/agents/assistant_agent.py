from fastapi import HTTPException
from app.utils.ai_helpers import determine_action_type
from app.utils.formatters import format_playwright_output, format_wiremock_output
from app.models.schemas import DevStyleResponse
import logging

logger = logging.getLogger(__name__)

def handle_assistant_message(message: str, action_type: str = None) -> DevStyleResponse:
    try:
        if not action_type:
            action_type = determine_action_type(message)

        if action_type == "playwright":
            from app.agents.playwright_agent import execute_playwright_test
            result = execute_playwright_test(message)
            return DevStyleResponse(
                text=format_playwright_output(result),
                data=result,
                success=True
            )
        elif action_type == "wiremock":
            from app.agents.wiremock_agent import create_and_start_wiremock_stub
            result = create_and_start_wiremock_stub(message)
            return DevStyleResponse(
                text=format_wiremock_output(result),
                data=result,
                success=True
            )
        else:
            raise ValueError(f"Unknown action type: {action_type}")
    except Exception as e:
        logger.error(f"Assistant error: {str(e)}")
        return DevStyleResponse(
            text=f"<div style='color:red; padding:10px; border:1px solid red'>🚨 {str(e)}</div>",
            success=False
        )