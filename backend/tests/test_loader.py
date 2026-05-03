import os
import tempfile
import pytest
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from rag.loader import load_document


def test_load_txt_file():
    content = "这是第一段。\n\n这是第二段。\n\n这是第三段。"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(content)
        f.flush()
        path = f.name

    try:
        result = load_document(path, "txt")
        assert len(result) > 0
        assert "第一段" in result
        assert "第二段" in result
    finally:
        os.unlink(path)


def test_load_md_file():
    content = "# 标题\n\n这是正文内容。\n\n## 子标题\n\n更多内容。"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        f.flush()
        path = f.name

    try:
        result = load_document(path, "md")
        assert len(result) > 0
        assert "标题" in result
    finally:
        os.unlink(path)


def test_load_csv_file():
    content = "name,age,city\nAlice,30,Beijing\nBob,25,Shanghai"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
        f.write(content)
        f.flush()
        path = f.name

    try:
        result = load_document(path, "csv")
        assert "Alice" in result
        assert "Beijing" in result
    finally:
        os.unlink(path)


def test_unsupported_type():
    with pytest.raises(ValueError, match="不支持的文件格式"):
        load_document("fake.xyz", "xyz")
