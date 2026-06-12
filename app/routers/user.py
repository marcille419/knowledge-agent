from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserRegister, UserLogin
from app.models.user import User
from app.database.db import get_db
from app.schemas.response import BaseResponse
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token
from app.core.deps import get_current_user

router = APIRouter(
    prefix = "/user",
    tags = ["user"]
)

@router.get("/info")
def get_user():
    return {
        "username" : "admin"
    }

@router.post("/register", response_model=BaseResponse)
def register(user:UserRegister, db:Session = Depends(get_db)):

    exist_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if exist_user:
        raise HTTPException(
            status_code = 400,
            detail = "用户已存在"
        )

    db_user = User(
        username = user.username,
        password = hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return BaseResponse(
        message = "注册成功",
        data = {
            "id" : db_user.id,
            "username" : db_user.username
        }
    )

@router.post("/login")
def login(user:UserLogin, db:Session = Depends(get_db)):
    db_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code = 400,
            detail="用户名或密码错误"
        )
    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code = 400,
            detail="用户名或密码错误"
        )

    token = create_access_token(
        {
            "user_id": db_user.id,
            "username": db_user.username
        }
    )

    return BaseResponse(
        message = "登陆成功",
        data = {
            "token" : token
        }
    )

@router.get("/profile")
def profile(current_user:User = Depends(get_current_user)):

    return BaseResponse(
        message = "获取用户信息成功",
        data = {
            "id" : current_user.id,
            "username" : current_user.username
        }
    )
