import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools.registry import ALL_TOOLS


def test_all_tools_registered():
    tool_names = [t.name for t in ALL_TOOLS]
    assert "rag_search" in tool_names
    assert "web_search" in tool_names
    assert "mysql_query" in tool_names


def test_tool_descriptions_not_empty():
    for t in ALL_TOOLS:
        assert t.description, f"Tool {t.name} has empty description"
