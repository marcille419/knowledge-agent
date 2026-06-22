import os
from charset_normalizer import from_path

def get_file_encoding(file_path: str) -> str:
    result = from_path(file_path).best()

    if result is None:
        return "utf-8"

    return result.encoding or "utf-8"

def parse_document(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        return parse_txt(file_path)
    if ext == ".md":
        return parse_md(file_path)

    raise ValueError("不支持的文件类型")

def parse_txt(file_path: str) -> str:
    encoding = get_file_encoding(file_path)
    with open(file_path, "r", encoding=encoding, errors="replace") as f:
        return f.read()

def parse_md(file_path: str) -> str:
    encoding = get_file_encoding(file_path)
    with open(file_path, "r", encoding=encoding, errors="replace") as f:
        return f.read()