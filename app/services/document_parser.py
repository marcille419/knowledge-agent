# TODO:
# 支持旧版 Word (.doc)

import os
import fitz
import logging

from charset_normalizer import from_path
from docx import Document

logger = logging.getLogger(__name__)

def get_file_encoding(file_path: str) -> str:
    result = from_path(file_path).best()

    if result is None:
        return "utf-8"

    return result.encoding or "utf-8"

def parse_txt(file_path: str) -> str:
    encoding = get_file_encoding(file_path)
    with open(file_path, "r", encoding=encoding, errors="replace") as f:
        return f.read()

def parse_md(file_path: str) -> str:
    encoding = get_file_encoding(file_path)
    with open(file_path, "r", encoding=encoding, errors="replace") as f:
        return f.read()

def parse_pdf(file_path: str) -> str:
    texts = []

    with fitz.open(file_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            try:
                texts.append(page.get_text("text"))
            except Exception as e:
                logger.warning(
                    "PDF页面解析失败: file=%s, page=%s, error=%s",
                    file_path,
                    page_num,
                    str(e)
                )
                continue

    if not texts:
        raise ValueError(
            "PDF解析失败"
        )

    return "\n".join(texts)

from docx import Document


def parse_docx(file_path: str) -> str:
    """
    TODO:
    - 支持表格解析
    - 支持页眉页脚
    - 支持图片OCR
    """

    texts = []

    doc = Document(file_path)

    for p in doc.paragraphs:
        if p.text.strip():
            texts.append(p.text)

    if not texts:
        raise ValueError(
            "DOCX内容为空"
        )

    return "\n".join(texts)


PARSERS = {
    ".txt": parse_txt,
    ".md": parse_md,
    ".pdf": parse_pdf,
    ".docx": parse_docx
}

def parse_document(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    parser = PARSERS.get(ext)

    if not parser:
        raise ValueError(f"不支持的文件类型: {ext}")

    return parser(file_path)

