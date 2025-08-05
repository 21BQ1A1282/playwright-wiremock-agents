import requests
import logging
from app.config import config  # Updated import

logger = logging.getLogger(__name__)

def create_wiremock_stub(stub_config: dict) -> dict:
    """Create a new WireMock stub"""
    try:
        response = requests.post(
            f"{config.WIREMOCK_URL}/__admin/mappings",  # Use config.WIREMOCK_URL
            json=stub_config,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"WireMock API error: {str(e)}")
        raise