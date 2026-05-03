from tools.registry import ALL_TOOLS


def get_tools_description() -> str:
    parts = []
    for tool in ALL_TOOLS:
        parts.append(f"- {tool.name}: {tool.description}")
    return "\n".join(parts)
