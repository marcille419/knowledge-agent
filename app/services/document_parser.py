import os
import fitz
import logging

from charset_normalizer import from_path

logger = logging.getLogger(__name__)

def get_file_encoding(file_path: str) -> str:
    result = from_path(file_path).best()

    if result is None:
        return "utf-8"

    return result.encoding or "utf-8"

def parse_document(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    PARSERS = {
        ".txt": parse_txt,
        ".md": parse_md,
        ".pdf": parse_pdf,
    }

    parser = PARSERS.get(ext)

    if not parser:
        raise ValueError(f"不支持的文件类型: {ext}")

    return parser(file_path)

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