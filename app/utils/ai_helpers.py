from openai import OpenAI
import os
import json
import re
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def call_openrouter(prompt: str, system_prompt: str = None) -> str:
    """Generic function to call OpenRouter API"""
    messages = [{"role": "user", "content": prompt}]
    if system_prompt:
        messages.insert(0, {"role": "system", "content": system_prompt})
    
    response = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content

def generate_ui_script(test_scenario: str) -> str:
    """Generate executable Playwright script without markdown"""
    system_prompt = """You are an expert Playwright test generator. Create a complete Python test script using Playwright sync API.
    Include all necessary imports and assertions. Return ONLY raw executable Python code WITHOUT markdown code blocks or explanations."""
    
    prompt = f"""Generate a Playwright test for: {test_scenario}
    Requirements:
    1. Use sync API (from playwright.sync_api import sync_playwright)
    2. Include proper assertions
    3. Handle page navigation
    4. Return ONLY the raw Python code
    5. NEVER include ```python or ``` marks"""
    
    script = call_openrouter(prompt, system_prompt)
    # Remove any remaining markdown artifacts
    return script.replace("```python", "").replace("```", "").strip()

def generate_wiremock_stub(description: str) -> dict:
    """Generate WireMock stub configuration"""
    system_prompt = """You are a WireMock configuration expert. Generate valid JSON stub configurations.
    Include request method, URL, and response status/body. Return ONLY JSON."""
    
    prompt = f"""Create WireMock stub for: {description}
    Requirements:
    1. Valid JSON format
    2. Include request and response
    3. Response must have status and body
    4. Return only the JSON configuration"""
    
    result = call_openrouter(prompt, system_prompt)
    return extract_json_from_response(result)

def extract_json_from_response(response: str) -> dict:
    """Extract JSON from AI response"""
    try:
        # Handle markdown code blocks
        match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        
        # Handle plain JSON
        match = re.search(r'{.*}', response, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        
        return json.loads(response)
    except json.JSONDecodeError:
        logger.error(f"Failed to parse JSON from: {response}")
        raise ValueError("Invalid JSON response from AI")

def determine_action_type(message: str) -> str:
    """Determine if message is for Playwright or WireMock"""
    prompt = f"""Classify this request:
    "{message}"
    Respond ONLY with either 'playwright' or 'wiremock'."""
    
    response = call_openrouter(prompt).strip().lower()
    if response not in ["playwright", "wiremock"]:
        raise ValueError("Could not determine action type")
    return response