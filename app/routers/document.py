import os
import uuid
from email.policy import default
from idlelib.query import Query

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