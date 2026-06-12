from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette import status

from app.database.db import get_db
from app.models.user import User
from app.utils.jwt import verify_token

security = HTTPBearer()

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
):
    token: str = credentials.credentials
    payload = verify_token(token)

    db_user = db.query(User).filter(
        User.id == payload['user_id']
    ).first()

    if not db_user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "用户不存在"
        )

    return db_user
