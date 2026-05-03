import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from rag.splitter import split_text


def test_split_long_text():
    text = "你好。" * 200
    chunks = split_text(text, chunk_size=200, chunk_overlap=20)
    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk) <= 200


def test_split_short_text():
    text = "这是一段很短的文本。"
    chunks = split_text(text, chunk_size=500, chunk_overlap=50)
    assert len(chunks) == 1
    assert chunks[0] == text


def test_split_empty_text():
    chunks = split_text("", chunk_size=500, chunk_overlap=50)
    assert len(chunks) == 0
