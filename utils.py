from time import time
import bcrypt
import jwt
from config import JWT_SECRET
from datetime import datetime, timezone
from fastapi import Header, HTTPException, Request
from log import log


def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def check_password(password: str, hashed: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)


def generate_jwt_token(user_id: int, username: str, expires_in: int = 3600*24*30) -> str:
    """生成jwt token

    Args:
        user_id (int): 用户编号
        username (str): 用户名
        expires_in (int, optional): 超时时间. Defaults to 3600*24*30.

    Returns:
        str: 返回生成的token
    """

    # 获取时间戳
    now = int(datetime.now(timezone.utc).timestamp())
    log.debug(now)

    return jwt.encode(payload={'user_id': user_id, 'username': username, 'exp': now + expires_in}, key=JWT_SECRET, algorithm='HS256')


def decode_jwt_token(token: str) -> dict:
    return jwt.decode(jwt=token, key=JWT_SECRET, algorithms=["HS256"])


def verify_token(Authorization: str = Header(), req: Request = None) -> dict | bool:
    if Authorization is None:
        return False

    try:
        token = Authorization.split(' ')[1]
        return decode_jwt_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail={
                            'status': 'error', 'message': 'token过期'})
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail={
                            'status': 'error', 'message': 'token无效'})
    except Exception as e:
        log.error(e)
        return False
