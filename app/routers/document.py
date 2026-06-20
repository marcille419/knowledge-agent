import os
import uuid
import logging
from email.policy import default
from idlelib.query import Query
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.document import Document
from app.models.user import User
from app.core.deps import get_current_user
from app.schemas.response import BaseResponse
from app.schemas.document import DocumentInfo, DocumentList

router = APIRouter(
    prefix = "/document",
    tags = ["document"]
)
UPLOAD_DIR = "app/uploads/documents"
MAX_FILE_SIZE = 1024 * 1024 * 20
ALLOWED_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".txt",
    ".md"
}
ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "text/markdown"
}

def get_file_size(file: UploadFile) -> int:
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    return file_size

@router.post("/upload", response_model = BaseResponse)
def upload_document(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # 创建目录,后续可以改成项目启动时统一创建目录
    os.makedirs(UPLOAD_DIR, exist_ok = True)

    # 检查文件大小
    file_size = get_file_size(file)
    if file_size > MAX_FILE_SIZE:
        raise  HTTPException(
            status_code = 400,
            detail = "文件大小超出限制"
        )

    # 文件后缀检查
    ext = os.path.splitext(file.filename)[1]
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code = 400,
            detail = "不支持的文件类型"
        )

    # Content-Type检查
    print(file.content_type)
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code = 400,
            detail = "非法文件类型"
        )

    # 生成唯一文件名
    stored_filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, stored_filename)

    # 下载文件
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    doc = Document(
        user_id = current_user.id,
        filename = file.filename,
        file_size=file_size,
        file_path = file_path,
        file_type = ext.lstrip(".")
    )

    db.add(doc)
    db.commit()
    db.refresh(doc)

    return BaseResponse(
        message = "上传成功",
        data = DocumentInfo.model_validate(doc)
    )

@router.get("/list", response_model = BaseResponse)
def get_document_list(
        page: int = Query(default = 1, ge = 1),
        size: int = Query(default = 10, ge = 1, le = 50),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    offset = (page - 1) * size

    query = (
        db.query(Document)
        .filter(Document.user_id == current_user.id)
    )

    total = query.count()

    documents = (
        query
        .order_by(Document.created_at.desc())
        .offset(offset)
        .limit(size)
        .all()
    )

    return BaseResponse(
        message = "获取成功",
        data = DocumentList(
            total = total,
            page = page,
            size = size,
            items = [
                DocumentInfo.model_validate(doc)
                for doc in documents
            ]
        )
    )

logger = logging.getLogger(__name__)
@router.delete("/{document_id}", response_model = BaseResponse)
def delete_document(
        document_id: int = Path(..., ge = 1, description = "要删除的文档id"),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    doc = (db.query(Document)
       .filter(Document.id == document_id,
               Document.user_id == current_user.id)
       .first()
    )

    if not doc:
        raise HTTPException(
            status_code = 404,
            detail = "文档不存在"
        )

    file_path = doc.file_path
    doc_id = doc.id

    try:
        db.delete(doc)
        db.commit()

    except Exception as e:
        db.rollback()
        logger.error(
            f"删除文档事务失败: document_id={document_id}, error={str(e)}",
            exc_info=True
        )
        raise HTTPException(
            status_code = 500,
            detail = "删除失败"
        )

    try:
        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        logger.warning(
            f"物理文件残留: user_id={current_user.id}, document_id={doc_id}, file_path={file_path}, error={str(e)}",
            exc_info=True
        )

    return BaseResponse(
        message = "删除成功"
    )