from app.database.base import Base
from app.database.db import engine

from app.models.user import User

Base.metadata.create_all(bind=engine)

print("表创建成功")