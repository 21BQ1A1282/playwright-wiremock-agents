from fastapi import APIRouter

router = APIRouter()

@router.get("/stubs")
def list_stubs():
    return {"message": "WireMock stubs endpoint"}