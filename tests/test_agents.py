import pytest
from app.agents.assistant_agent import handle_assistant_message

def test_playwright_flow():
    response = handle_assistant_message("Test login page", "playwright")
    assert "text" in response
    assert "data" in response
    assert "<table" in response.text  # Verify HTML output

def test_wiremock_flow():
    response = handle_assistant_message("Mock GET /api/users", "wiremock")
    assert "WireMock" in response.text
    assert "generated_stub_config" in response.data