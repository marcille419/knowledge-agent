from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.base import Base

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    __table_args__ = (
        UniqueConstraint(
            'document_id',
            'chunk_index',
            name = 'uq_document_chunk'
        ),
    )

    id = Column(Integer, primary_key = True, index = True)

    document_id = Column(
        Integer,
        ForeignKey('documents.id', ondelete = "CASCADE"),
        nullable = False,
        index = True
    )

    chunk_index = Column(Integer, nullable = False)
    content = Column(Text, nullable = False)
    created_at = Column(DateTime, server_default = func.now())

    document = relationship(
        "Document",
        back_populates="chunks"
    )