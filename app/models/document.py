from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.base import Base

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key = True, index = True)

    user_id = Column(
        Integer,
        ForeignKey('users.id', ondelete = "CASCADE"),
        nullable = False,
        index = True
        )

    filename = Column(String(255), nullable = False)
    file_path = Column(String(500), nullable = False)
    file_type = Column(String(50), nullable = False)
    file_size = Column(BigInteger, nullable=False)

    created_at = Column(DateTime, server_default = func.now())

    chunks = relationship(
        "DocumentChunk",
        back_populates = "document",
        cascade = "all, delete-orphan"
    )