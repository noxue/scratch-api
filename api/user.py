
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from log import log
from models.models import User, session
from utils import generate_jwt_token, hash_password, check_password, verify_token

router = APIRouter(
    prefix="/users",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


class RegisterUser(BaseModel):
    username: str
    password: str


@router.post("/register")
async def register(user: RegisterUser):
    import re

    r = re.compile(r"^[a-zA-Z0-9_]{1,15}$")
    if not r.match(user.username):
        return {"status": "error", "message": "用户名只能包含数字字母下划线，最长15字符"}

    r = re.compile(r"^[a-zA-Z0-9_\.\-,/\?!@#\$%\^&*\(\)\[\]|]{5,50}$")
    if not r.match(user.password):
        return {"status": "error", "message": "密码长度5-50个字符，可包含字母数字以及特殊字符"}


    if session.query(User).filter(User.username == user.username).count():
        return {"status": "error", "message": "用户名已存在"}

    try:
        user = User(username=user.username,
                    password=hash_password(user.password))
        session.add(user)
        session.commit()
        return {"status": "ok", "message": "注册成功"}
    except Exception as e:
        log.error(e)
        return {"status": "error", "message": "注册失败"}


class LoginUser(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(user: LoginUser):
    u: User = session.query(User).filter(
        User.username == user.username).first()
    if not u:
        return {"status": "error", "message": "用户名不存在"}

    if not check_password(user.password, session.query(User).filter(User.username == user.username).first().password):
        return {"status": "error", "message": "密码错误"}
    token = generate_jwt_token(u.id, u.username)
    return {"status": "ok", "message": "登录成功", "data": {"token": token, "username": u.username, "uid": u.id}}


@router.get('/me')
async def get_me(info: dict = Depends(verify_token)):
    if not info:
        return {"status": "error", "message": "token无效"}
    return {"status": "ok", "message": "获取成功", "data": info}
