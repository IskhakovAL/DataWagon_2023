from fastapi import APIRouter


router = APIRouter(prefix="/api/debug")


@router.get("/")
def debug():
    return "ok"
