import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    WIREMOCK_URL = os.getenv("WIREMOCK_URL", "http://localhost:8080")
    
    # Playwright Configuration
    PLAYWRIGHT_HEADLESS = os.getenv("PLAYWRIGHT_HEADLESS", "true").lower() == "true"
    PLAYWRIGHT_TIMEOUT = int(os.getenv("PLAYWRIGHT_TIMEOUT", "30000"))  # milliseconds

# Singleton configuration instance
config = Config()