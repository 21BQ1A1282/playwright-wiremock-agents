import os
import tempfile
import subprocess
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def run_playwright_script(script: str, scenario: str) -> dict:
    """Execute Playwright script with visible browser"""
    try:
        # Force visible browser in the script
        modified_script = script.replace(
            "browser = p.chromium.launch()",
            "browser = p.chromium.launch(headless=False, slow_mo=500)"  # Visible + slow motion
        )
        
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
            f.write(modified_script.encode())
            filepath = f.name
        
        # Standard subprocess call (no platform-specific commands)
        result = subprocess.run(
            ["python", filepath],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        os.unlink(filepath)
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "return_code": result.returncode
        }
    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "return_code": -1
        }