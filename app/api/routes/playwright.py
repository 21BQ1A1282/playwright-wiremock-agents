from fastapi import APIRouter

router = APIRouter()

@router.get("/tests")
def list_tests():
    return {"message": "Playwright tests endpoint"}