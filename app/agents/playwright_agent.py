from app.utils.ai_helpers import generate_ui_script
from app.services.playwright_runner import run_playwright_script
import logging
import uuid

logger = logging.getLogger(__name__)

def execute_playwright_test(test_scenario: str) -> dict:
    """Execute test with visible browser (no video)"""
    try:
        # Generate basic script
        script = generate_ui_script(test_scenario)
        
        # Execute with visible browser
        execution_result = run_playwright_script(script, test_scenario)
        
        return {
            "action": "playwright",
            "test_id": f"pw_{uuid.uuid4().hex[:6]}",
            "test_scenario": test_scenario,
            "execution_result": execution_result
        }
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise