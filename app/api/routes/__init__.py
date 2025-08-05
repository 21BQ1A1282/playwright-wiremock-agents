from fastapi import APIRouter
from .assistant import router as assistant_router
from .playwright import router as playwright_router
from .wiremock import router as wiremock_router

router = APIRouter()

router.include_router(assistant_router, prefix="/assistant", tags=["Assistant"])
router.include_router(playwright_router, prefix="/playwright", tags=["Playwright"])
router.include_router(wiremock_router, prefix="/wiremock", tags=["WireMock"])