from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage, ToolMessage
from config import settings
from agents.state import AgentState
from prompts.system import get_system_prompt
from tools.registry import ALL_TOOLS, TOOL_MAP


def get_llm():
    """获取绑定了工具的 DeepSeek LLM。"""
    llm = ChatOpenAI(
        model=settings.DEEPSEEK_MODEL,
        api_key=settings.DEEPSEEK_API_KEY,
        base_url=settings.DEEPSEEK_BASE_URL,
        temperature=0.7,
        streaming=True,
    )
    return llm.bind_tools(ALL_TOOLS)


def agent_node(state: AgentState) -> dict:
    """Agent 节点：LLM 分析消息，决定下一步（回答或调用工具）。"""
    messages = state["messages"]

    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=get_system_prompt())] + messages

    llm = get_llm()
    response = llm.invoke(messages)

    return {"messages": [response]}


def tool_node(state: AgentState) -> dict:
    """Tool 节点：执行 Agent 请求的工具调用。"""
    last_message: AIMessage = state["messages"][-1]
    tool_messages = []

    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_id = tool_call["id"]

        tool_func = TOOL_MAP.get(tool_name)
        if tool_func is None:
            result = f"错误：未找到工具 {tool_name}"
        else:
            try:
                result = tool_func(**tool_args)
            except Exception as e:
                result = f"工具执行错误：{str(e)}"

        tool_messages.append(
            ToolMessage(content=str(result), tool_call_id=tool_id)
        )

    count = state.get("tool_call_count", 0) + 1

    return {"messages": tool_messages, "tool_call_count": count}


def should_continue(state: AgentState) -> str:
    """条件路由：决定是否继续调用工具。"""
    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        if state.get("tool_call_count", 0) >= state.get("max_tool_calls", 5):
            return "end"
        return "tools"

    return "end"
