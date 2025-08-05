import json
from typing import Dict, Any

def format_playwright_output(result: Dict[str, Any]) -> str:
    status = "PASSED" if result["execution_result"]["success"] else "FAILED"
    color = "green" if status == "PASSED" else "red"
    
    return f"""
    <div style='font-family: Arial; margin: 10px;'>
      <h3>🎯 Playwright Test Results</h3>
      <table border='1' cellpadding='5'>
        <tr><td><b>Scenario</b></td><td>{result['test_scenario']}</td></tr>
        <tr><td><b>Status</b></td><td><span style='color:{color}; font-weight:bold'>{status}</span></td></tr>
        <tr><td><b>Output</b></td><td><pre>{result['execution_result']['output']}</pre></td></tr>
      </table>
    </div>
    """

def format_wiremock_output(result: Dict[str, Any]) -> str:
    return f"""
    <div style='font-family: Arial; margin: 10px;'>
      <h3>🔌 WireMock Stub</h3>
      <table border='1' cellpadding='5'>
        <tr><td><b>Method</b></td><td>{result['generated_stub_config']['request']['method']}</td></tr>
        <tr><td><b>URL</b></td><td>{result['generated_stub_config']['request']['url']}</td></tr>
        <tr><td><b>Response</b></td><td>HTTP {result['generated_stub_config']['response']['status']}</td></tr>
      </table>
      <pre>{json.dumps(result['generated_stub_config'], indent=2)}</pre>
    </div>
    """