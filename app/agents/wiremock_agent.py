from app.utils.ai_helpers import generate_wiremock_stub
from app.services.wiremock_client import create_wiremock_stub
import logging
import json

logger = logging.getLogger(__name__)

def create_and_start_wiremock_stub(description: str) -> dict:
    try:
        # Generate stub configuration
        stub_config = generate_wiremock_stub(description)
        
        # Ensure body is stringified JSON
        if isinstance(stub_config['response'].get('body'), dict):
            stub_config['response']['body'] = json.dumps(stub_config['response']['body'])
        
        # Create the stub
        creation_result = create_wiremock_stub(stub_config)
        
        return {
            "action": "wiremock",
            "description": description,
            "generated_stub_config": stub_config,
            "creation_result": creation_result
        }
    except Exception as e:
        logger.error(f"WireMock stub creation failed: {str(e)}")
        raise