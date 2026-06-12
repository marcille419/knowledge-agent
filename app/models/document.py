from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.sql import func

from app.database.base import Base

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key = True, index = True)

    user_id = Column(Integer,
                     ForeignKey('users.id', ondelete = "CASCADE"),
                     nullable = False
                     )

    filename = Column(String(255), nullable = False)
    file_path = Column(String(500), nullable = False)
    file_type = Column(String(50), nullable = False)
    file_size = Column(BigInteger, nullable=False)

    created_at = Column(DateTime, server_default = func.now())