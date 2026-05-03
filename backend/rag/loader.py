import csv


def load_document(file_path: str, file_type: str) -> str:
    """根据文件类型加载文档，返回纯文本内容。"""
    loaders = {
        "txt": _load_txt,
        "md": _load_markdown,
        "csv": _load_csv,
        "pdf": _load_pdf,
        "docx": _load_docx,
    }

    loader = loaders.get(file_type)
    if not loader:
        raise ValueError(f"不支持的文件格式: {file_type}")

    return loader(file_path)


def _load_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def _load_markdown(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def _load_csv(file_path: str) -> str:
    lines = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return ""
        for row in reader:
            parts = [f"{col}：{val}" for col, val in row.items()]
            lines.append("，".join(parts))
    return "\n".join(lines)


def _load_pdf(file_path: str) -> str:
    import fitz
    doc = fitz.open(file_path)
    text_parts = []
    for page in doc:
        text_parts.append(page.get_text())
    doc.close()
    return "\n\n".join(text_parts)


def _load_docx(file_path: str) -> str:
    from docx import Document
    doc = Document(file_path)
    return "\n\n".join([para.text for para in doc.paragraphs if para.text.strip()])
