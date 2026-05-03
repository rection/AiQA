from langgraph.graph import MessagesState


class AgentState(MessagesState):
    """ReAct Agent 的图状态。MessagesState 自带 messages: list[BaseMessage]。"""
    session_id: str = ""
    tool_call_count: int = 0
    max_tool_calls: int = 5
