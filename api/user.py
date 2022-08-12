
from fastapi import APIRouter
from pydantic import BaseModel
from log import get_logger

logger = get_logger()

logger.debug("ssss")

router = APIRouter(
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

class RegisterUser(BaseModel):
    username: str
    password: str
    password_confirm: str


@router.get("/register")
async def register(user: RegisterUser):
    '''
    注册用户
    '''
    logger.debug(user)
    
    return {"status": "ok"}
