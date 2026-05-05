问答助手 — 系统设计文档

> 版本：v1.0 | 日期：2026-05-03

---

## 一、项目概述

构建一个基于 LangChain + LangGraph 的 AI 问答助手，支持文档上传与 RAG 检索、网络搜索、MySQL 数据库查询，通过 ReAct Agent 模式智能调度工具，使用 FastAPI 提供 SSE 流式接口，Vue 3 构建深色主题聊天界面。

### 核心能力

| 能力 | 说明 |
|------|------|
| 文档问答 | 上传 PDF/Word/Markdown/TXT/CSV，基于 RAG 检索回答 |
| 网络搜索 | 通过 Tavily API 联网搜索实时信息 |
| 数据库查询 | 自然语言转 SQL，查询 MySQL 数据库 |
| 多轮对话 | 支持上下文记忆的多轮对话 |
| 流式输出 | SSE 逐字输出，实时反馈 Agent 工具调用状态 |

---

## 二、技术栈

### 后端

| 组件 | 技术选型 | 版本 |
|------|---------|------|
| Web 框架 | FastAPI | >= 0.110 |
| LLM | DeepSeek (deepseek-chat) | - |
| Agent 框架 | LangGraph | >= 0.2 |
| Chain 框架 | LangChain | >= 0.3 |
| 向量数据库 | ChromaDB | >= 0.5 |
| 网络搜索 | Tavily API | - |
| 数据库 | MySQL + SQLAlchemy | - |
| 文档解析 | PyMuPDF (PDF)、python-docx (Word)、markdown | - |
| Embedding | DeepSeek Embedding API | - |

### 前端

| 组件 | 技术选型 | 版本 |
|------|---------|------|
| 框架 | Vue 3 + Composition API | >= 3.4 |
| 构建工具 | Vite | >= 5.0 |
| UI 风格 | 深色主题 + 玻璃拟态 | - |
| Markdown 渲染 | markdown-it + highlight.js | - |
| HTTP 请求 | Axios | - |
| 流式连接 | EventSource (SSE) | - |

---

## 三、整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                       Vue 3 前端                             │
│                                                              │
│  ┌──────────┐   ┌──────────────────┐   ┌────────────────┐   │
│  │ Sidebar   │   │   ChatArea       │   │ DocumentPanel  │   │
│  │ 历史会话  │   │   消息流 + SSE   │   │ 文档上传/列表  │   │
│  └──────────┘   └──────────────────┘   └────────────────┘   │
│                                                              │
└──────────────────────────┬───────────────────────────────────┘
                           │ HTTP / SSE
┌──────────────────────────┴───────────────────────────────────┐
│                       FastAPI 后端                           │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              LangGraph ReAct Agent                   │    │
│  │                                                      │    │
│  │   START → Agent 节点 → 条件路由 → 工具节点 → Agent   │    │
│  │                  ↑                      │             │    │
│  │                  └──────────────────────┘             │    │
│  │                                                      │    │
│  └──────────────────────┬──────────────────────────────┘    │
│                         │                                    │
│  ┌──────────┬───────────┼───────────────┬──────────────┐    │
│  │          │           │               │              │    │
│  ▼          ▼           ▼               ▼              ▼    │
│ RAG工具   搜索工具   MySQL工具     文档加载器     Embedding  │
│  │          │                                             │  │
│  ▼          ▼                                             │  │
│ ChromaDB  Tavily API                      DeepSeek API    │  │
│                                                      MySQL  │
└──────────────────────────────────────────────────────────────┘
```

---

## 四、后端目录结构

```
backend/
├── main.py                     # FastAPI 应用入口
├── config.py                   # 环境变量配置（Pydantic Settings）
├── routers/
│   ├── chat.py                 # 聊天相关接口
│   ├── document.py             # 文档上传/管理接口
│   └── health.py               # 健康检查
├── agents/
│   ├── graph.py                # LangGraph 图定义
│   ├── nodes.py                # 节点实现（agent_node、tool_node）
│   └── state.py                # AgentState 类型定义
├── tools/
│   ├── rag_tool.py             # RAG 检索工具
│   ├── search_tool.py          # 网络搜索工具
│   ├── db_tool.py              # MySQL 查询工具
│   └── registry.py             # 工具注册表
├── rag/
│   ├── loader.py               # 文档加载（多格式解析）
│   ├── splitter.py             # 文本分块策略
│   ├── embeddings.py           # DeepSeek Embedding 封装
│   └── vectorstore.py          # ChromaDB CRUD 操作
├── prompts/
│   ├── system.py               # 系统提示词
│   ├── react.py                # ReAct Agent 提示词模板
│   └── tools_description.py    # 工具描述（注入 Agent）
├── models/
│   └── schemas.py              # Pydantic 请求/响应模型
├── database/
│   ├── session.py              # SQLAlchemy 引擎与会话
│   └── models.py               # 会话/消息数据库模型
└── services/
    ├── chat_service.py         # 对话业务逻辑编排
    └── document_service.py     # 文档处理业务逻辑
```

---

## 五、前端目录结构

```
frontend/
├── index.html
├── package.json
├── vite.config.js
├── src/
│   ├── main.js                 # 入口
│   ├── App.vue                 # 根组件
│   ├── views/
│   │   └── ChatView.vue        # 主页面（三栏布局）
│   ├── components/
│   │   ├── Sidebar.vue         # 左侧栏：新对话 + 历史列表 + 文档入口
│   │   ├── ChatArea.vue        # 中间：消息列表 + SSE 流式渲染
│   │   ├── MessageBubble.vue   # 单条消息气泡（用户/AI）
│   │   ├── MarkdownRenderer.vue# Markdown 渲染（代码高亮、表格）
│   │   ├── InputBox.vue        # 底部输入框 + 上传按钮 + 发送
│   │   ├── ToolIndicator.vue   # 工具调用状态提示条
│   │   └── DocumentPanel.vue   # 右侧栏：文档列表 + 上传弹窗
│   ├── composables/
│   │   ├── useSSE.js           # SSE 流式连接管理
│   │   ├── useChat.js          # 聊天状态（消息列表、发送逻辑）
│   │   └── useDocument.js      # 文档上传/列表管理
│   ├── api/
│   │   └── index.js            # Axios 实例 + API 封装
│   ├── stores/
│   │   └── chat.js             # Pinia 状态管理
│   └── styles/
│       ├── variables.css       # CSS 变量（颜色、圆角）
│       └── global.css          # 全局样式
```

---

## 六、接口设计

### 6.1 聊天接口

#### POST /api/chat/stream — 流式对话

发起对话，通过 SSE 流式返回 Agent 思考过程和回答。

**请求头：**

```
Content-Type: application/json
Accept: text/event-stream
```

**请求体：**

```json
{
  "session_id": "uuid-string",
  "message": "帮我查询用户表中有多少条记录？",
  "stream": true
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| session_id | string | 是 | 会话 ID，新建传空串自动创建 |
| message | string | 是 | 用户消息内容 |
| stream | bool | 否 | 是否流式输出，默认 true |

**SSE 响应事件流：**

```
event: session
data: {"session_id": "abc-123", "created": true}

event: thinking
data: {"content": "我需要查询数据库来回答这个问题"}

event: tool_call
data: {"tool": "mysql_query", "input": "SELECT COUNT(*) FROM users", "status": "running"}

event: tool_result
data: {"tool": "mysql_query", "output": "查询结果：共 15,234 条记录", "status": "success"}

event: answer
data: {"content": "根据查询结果，用户表中共有 **15,234** 条记录。"}

event: answer
data: {"content": "如果您需要更详细的统计信息"}

event: answer
data: {"content": "（如按日期分组），请告诉我。"}

event: done
data: {"message_id": "msg-456", "tokens_used": 342}
```

**事件类型说明：**

| event | data 结构 | 说明 |
|-------|----------|------|
| session | `{session_id, created}` | 返回会话 ID |
| thinking | `{content}` | Agent 思考过程片段 |
| tool_call | `{tool, input, status}` | 工具调用开始（status=running） |
| tool_result | `{tool, output, status}` | 工具调用结果（status=success/error） |
| answer | `{content}` | 最终回答片段（多次发送） |
| done | `{message_id, tokens_used}` | 回答完成 |
| error | `{code, message}` | 错误信息 |

---

#### GET /api/chat/sessions — 获取会话列表

**请求：**

```
GET /api/chat/sessions?page=1&page_size=20
```

**响应：**

```json
{
  "total": 15,
  "page": 1,
  "page_size": 20,
  "sessions": [
    {
      "session_id": "abc-123",
      "title": "用户表统计查询",
      "created_at": "2026-05-03T10:30:00",
      "updated_at": "2026-05-03T10:35:00",
      "message_count": 8
    }
  ]
}
```

---

#### GET /api/chat/sessions/{session_id}/messages — 获取会话历史

**请求：**

```
GET /api/chat/sessions/abc-123/messages?page=1&page_size=50
```

**响应：**

```json
{
  "session_id": "abc-123",
  "total": 8,
  "messages": [
    {
      "message_id": "msg-001",
      "role": "user",
      "content": "帮我查询用户表中有多少条记录？",
      "created_at": "2026-05-03T10:30:00"
    },
    {
      "message_id": "msg-002",
      "role": "assistant",
      "content": "根据查询结果，用户表中共有 **15,234** 条记录。",
      "tool_calls": [
        {
          "tool": "mysql_query",
          "input": "SELECT COUNT(*) FROM users",
          "output": "查询结果：共 15,234 条记录"
        }
      ],
      "created_at": "2026-05-03T10:30:05"
    }
  ]
}
```

---

#### DELETE /api/chat/sessions/{session_id} — 删除会话

**响应：**

```json
{
  "deleted": true,
  "session_id": "abc-123"
}
```

---

### 6.2 文档接口

#### POST /api/documents/upload — 上传文档

**请求头：**

```
Content-Type: multipart/form-data
```

**请求体（form-data）：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | File | 是 | 文档文件（PDF/Word/MD/TXT/CSV） |
| session_id | string | 否 | 绑定到指定会话，不传则全局可用 |

**响应：**

```json
{
  "document_id": "doc-789",
  "filename": "产品需求文档.pdf",
  "file_size": 204800,
  "file_type": "pdf",
  "chunk_count": 45,
  "status": "indexed",
  "created_at": "2026-05-03T11:00:00"
}
```

**状态说明：**

| status | 含义 |
|--------|------|
| processing | 正在解析和向量化 |
| indexed | 已完成索引，可用于问答 |
| failed | 处理失败 |

---

#### GET /api/documents — 获取文档列表

**请求：**

```
GET /api/documents?session_id=abc-123&page=1&page_size=20
```

**响应：**

```json
{
  "total": 5,
  "documents": [
    {
      "document_id": "doc-789",
      "filename": "产品需求文档.pdf",
      "file_size": 204800,
      "file_type": "pdf",
      "chunk_count": 45,
      "status": "indexed",
      "created_at": "2026-05-03T11:00:00"
    }
  ]
}
```

---

#### DELETE /api/documents/{document_id} — 删除文档

从 ChromaDB 中删除该文档的所有向量块。

**响应：**

```json
{
  "deleted": true,
  "document_id": "doc-789",
  "chunks_deleted": 45
}
```

---

### 6.3 健康检查

#### GET /api/health

**响应：**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "deepseek_api": "ok",
    "chromadb": "ok",
    "mysql": "ok"
  }
}
```

---

## 七、数据模型（Pydantic）

### 7.1 请求模型

```python
# models/schemas.py

class ChatRequest(BaseModel):
    session_id: str = ""
    message: str
    stream: bool = True

class DocumentUpload(BaseModel):
    session_id: str = ""
```

### 7.2 响应模型

```python
class SessionInfo(BaseModel):
    session_id: str
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int

class MessageInfo(BaseModel):
    message_id: str
    role: str              # "user" | "assistant"
    content: str
    tool_calls: list[ToolCall] | None = None
    created_at: datetime

class ToolCall(BaseModel):
    tool: str
    input: str
    output: str

class DocumentInfo(BaseModel):
    document_id: str
    filename: str
    file_size: int
    file_type: str
    chunk_count: int
    status: str            # "processing" | "indexed" | "failed"
    created_at: datetime

class SSEEvent(BaseModel):
    event: str             # "session" | "thinking" | "tool_call" | "tool_result" | "answer" | "done" | "error"
    data: dict
```

### 7.3 LangGraph 状态模型

```python
# agents/state.py
from langgraph.graph import MessagesState

class AgentState(MessagesState):
    """ReAct Agent 的图状态"""
    # MessagesState 自带 messages: list[BaseMessage]
    # 扩展字段：
    session_id: str
    document_ids: list[str]     # 本次会话关联的文档 ID
    tool_call_count: int        # 工具调用计数（防止无限循环）
    max_tool_calls: int = 5     # 最大工具调用次数
```

---

## 八、数据库设计

### 8.1 会话表（sessions）

```sql
CREATE TABLE sessions (
    id          VARCHAR(36) PRIMARY KEY,
    title       VARCHAR(200) NOT NULL DEFAULT '',
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 8.2 消息表（messages）

```sql
CREATE TABLE messages (
    id          VARCHAR(36) PRIMARY KEY,
    session_id  VARCHAR(36) NOT NULL,
    role        ENUM('user', 'assistant') NOT NULL,
    content     TEXT NOT NULL,
    tool_calls  JSON DEFAULT NULL,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_session (session_id),
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);
```

### 8.3 文档表（documents）

```sql
CREATE TABLE documents (
    id          VARCHAR(36) PRIMARY KEY,
    session_id  VARCHAR(36) DEFAULT NULL,
    filename    VARCHAR(255) NOT NULL,
    file_path   VARCHAR(500) NOT NULL,
    file_size   INT NOT NULL,
    file_type   VARCHAR(20) NOT NULL,
    chunk_count INT NOT NULL DEFAULT 0,
    status      ENUM('processing', 'indexed', 'failed') NOT NULL DEFAULT 'processing',
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_session (session_id)
);
```

---

## 九、LangGraph ReAct Agent 设计

### 9.1 图结构

```
                    ┌──────────┐
            ┌────── │   START   │
            │       └────┬─────┘
            │            ▼
            │    ┌───────────────┐
            │    │   Agent Node   │  ← LLM 分析问题，决定下一步
            │    └───────┬───────┘
            │            │
            │    ┌───────▼───────┐
            │    │  Should Tool?  │  ← 条件路由
            │    └───┬───────┬───┘
            │   yes  │       │ no
            │        ▼       ▼
            │  ┌──────────┐ ┌────────┐
            │  │Tool Node  │ │  END   │
            │  │执行工具   │ └────────┘
            │  └─────┬────┘
            │        │
            └────────┘  （结果回到 Agent Node 继续推理）
```

### 9.2 节点定义

**Agent Node（agent_node）**

- 输入：`AgentState.messages`（对话历史）
- 调用：DeepSeek Chat API（绑定工具 schema）
- 输出：AIMessage（可能包含 tool_calls）
- 提示词：ReAct 系统提示词 + 工具描述

**Tool Node（tool_node）**

- 输入：`AIMessage.tool_calls`
- 执行：根据 tool name 路由到对应工具函数
- 输出：`ToolMessage`（工具结果）
- 工具映射：

```python
TOOL_MAP = {
    "rag_search": rag_tool.search,
    "web_search": search_tool.search,
    "mysql_query": db_tool.query,
}
```

**条件路由（should_continue）**

```python
def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    # 如果 Agent 发起了工具调用
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        # 检查调用次数上限
        if state.get("tool_call_count", 0) >= state.get("max_tool_calls", 5):
            return "end"
        return "tools"
    return "end"
```

### 9.3 工具注册

```python
from langchain_core.tools import tool

@tool
def rag_search(query: str, document_ids: list[str] = None) -> str:
    """在已上传的文档中搜索相关内容。当用户问题涉及已上传文档时使用此工具。
    Args:
        query: 搜索查询语句
        document_ids: 限定搜索的文档 ID 列表，不传则搜索所有文档
    """
    # ChromaDB 相似度搜索
    results = vectorstore.similarity_search(query, k=5, filter=...)
    return format_results(results)

@tool
def web_search(query: str) -> str:
    """搜索互联网获取实时信息。当用户问题涉及实时数据、新闻、或文档中没有的信息时使用。
    Args:
        query: 搜索关键词
    """
    results = tavily_client.search(query)
    return format_results(results)

@tool
def mysql_query(natural_language: str) -> str:
    """将自然语言转换为 SQL 并执行查询。当用户需要查询数据库中的数据时使用。
    Args:
        natural_language: 用自然语言描述要查询的内容
    """
    sql = llm.convert_to_sql(natural_language)
    result = db.execute(sql)
    return format_result(result)
```

---

## 十、RAG 检索流程

### 10.1 文档处理管道

```
上传文件 → 识别文件类型 → 选择解析器 → 文本清洗 → 分块 → Embedding → 存储
```

**文件解析器选择：**

| 文件类型 | 解析库 | 说明 |
|---------|--------|------|
| .pdf | PyMuPDF (fitz) | 提取文本，保留段落结构 |
| .docx | python-docx | 按段落提取文本 |
| .md | markdown + 自定义 | 解析 Markdown 结构 |
| .txt | 直接读取 | 编码自动检测 |
| .csv | pandas | 转为文本描述 |

**分块策略：**

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,          # 每块 500 字符
    chunk_overlap=50,        # 重叠 50 字符
    separators=["\n\n", "\n", "。", ".", " ", ""],
    length_function=len,
)
```

**Embedding：**

- 调用 DeepSeek Embedding API
- 模型：`deepseek-embedding`
- 维度：1536

### 10.2 检索流程

```
用户问题 → DeepSeek Embedding → ChromaDB 相似度搜索 → top-5 结果 → 组装上下文
```

```python
def rag_tool.search(query: str, document_ids: list[str] = None) -> str:
    # 1. 查询向量化
    query_embedding = embedding_model.embed_query(query)

    # 2. ChromaDB 检索
    filter_dict = {"document_id": {"$in": document_ids}} if document_ids else None
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        where=filter_dict,
    )

    # 3. 格式化返回
    context = "\n\n---\n\n".join([
        f"[来源: {doc.metadata['filename']}]\n{doc.page_content}"
        for doc in results
    ])
    return context
```

---

## 十一、提示词设计

### 11.1 系统提示词

```python
SYSTEM_PROMPT = """你是一个专业的 AI 问答助手，能够基于文档、网络搜索和数据库查询来回答用户问题。

## 核心原则
1. 优先使用已上传文档中的信息回答问题
2. 如果文档中没有相关信息，再使用网络搜索
3. 数据库查询需要用户明确提到数据相关需求
4. 所有回答必须基于事实，不要编造信息
5. 引用来源时请注明文档名称或搜索来源

## 回答格式
- 使用 Markdown 格式
- 代码块标注语言类型
- 表格整理结构化数据
- 适当使用引用块标注来源

## 工具使用规则
- 使用 ReAct 模式：Thought → Action → Observation
- 每次只调用一个工具
- 根据工具结果决定是否需要进一步操作
- 最多调用 {max_tool_calls} 次工具
"""
```

### 11.2 ReAct 提示词

```python
REACT_PROMPT = """你可以使用以下工具来回答问题：

{tools_description}

请按照以下格式：

Question: 用户的问题
Thought: 我需要思考如何回答这个问题
Action: 工具名称
Action Input: 工具输入参数
Observation: 工具返回结果
... （可以重复多次 Thought/Action/Action Input/Observation）
Thought: 我现在知道答案了
Final Answer: 最终回答

重要：每次只调用一个工具。当信息足够时，直接给出 Final Answer。
"""
```

### 11.3 工具描述提示词

每个工具的描述通过 `@tool` 装饰器的 docstring 自动生成，注入到 Agent 的 tools schema 中。

---

## 十二、流式输出协议

### 12.1 SSE 事件类型

```python
class SSEEventType:
    SESSION = "session"           # 返回会话 ID
    THINKING = "thinking"         # Agent 思考过程
    TOOL_CALL = "tool_call"       # 工具调用开始
    TOOL_RESULT = "tool_result"   # 工具调用结果
    ANSWER = "answer"             # 回答片段
    DONE = "done"                 # 完成
    ERROR = "error"               # 错误
```

### 12.2 后端 SSE 发送

```python
from fastapi.responses import StreamingResponse

async def generate_sse(session_id: str, message: str):
    # 1. 发送会话 ID
    yield sse_encode("session", {"session_id": session_id})

    # 2. 运行 LangGraph Agent，流式输出
    async for event in graph.astream_events(
        input={"messages": [HumanMessage(content=message)]},
        config={"configurable": {"session_id": session_id}},
    ):
        if event["event"] == "on_chat_model_stream":
            chunk = event["data"]["chunk"]
            if chunk.content:
                yield sse_encode("answer", {"content": chunk.content})

        elif event["event"] == "on_tool_start":
            yield sse_encode("tool_call", {
                "tool": event["name"],
                "input": str(event["data"].get("input", "")),
                "status": "running"
            })

        elif event["event"] == "on_tool_end":
            yield sse_encode("tool_result", {
                "tool": event["name"],
                "output": str(event["data"].get("output", ""))[:500],
                "status": "success"
            })

    # 3. 发送完成
    yield sse_encode("done", {"message_id": msg_id})

def sse_encode(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"
```

### 12.3 前端 SSE 接收

```javascript
// composables/useSSE.js
export function useSSE() {
  function connect(url, body, callbacks) {
    const es = new EventSource(
      `${url}?${new URLSearchParams(body)}`
    );

    es.addEventListener('session', (e) => {
      callbacks.onSession?.(JSON.parse(e.data));
    });
    es.addEventListener('thinking', (e) => {
      callbacks.onThinking?.(JSON.parse(e.data));
    });
    es.addEventListener('tool_call', (e) => {
      callbacks.onToolCall?.(JSON.parse(e.data));
    });
    es.addEventListener('tool_result', (e) => {
      callbacks.onToolResult?.(JSON.parse(e.data));
    });
    es.addEventListener('answer', (e) => {
      callbacks.onAnswer?.(JSON.parse(e.data));
    });
    es.addEventListener('done', (e) => {
      callbacks.onDone?.(JSON.parse(e.data));
      es.close();
    });
    es.addEventListener('error', (e) => {
      callbacks.onError?.(JSON.parse(e.data));
      es.close();
    });

    return es;
  }

  return { connect };
}
```

> **注意**：由于 EventSource 不支持自定义 POST body，实际实现中使用 `fetch` + `ReadableStream` 解析 SSE 流：
>
> ```javascript
> const response = await fetch('/api/chat/stream', {
>   method: 'POST',
>   headers: { 'Content-Type': 'application/json' },
>   body: JSON.stringify({ session_id, message, stream: true }),
> });
> const reader = response.body.getReader();
> // 按行解析 SSE 格式
> ```

---

## 十三、配置管理

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # DeepSeek
    DEEPSEEK_API_KEY: str
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"
    DEEPSEEK_MODEL: str = "deepseek-chat"
    DEEPSEEK_EMBEDDING_MODEL: str = "deepseek-embedding"

    # Tavily 搜索
    TAVILY_API_KEY: str

    # MySQL
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str = "ai_assistant"

    # ChromaDB
    CHROMA_PERSIST_DIR: str = "./chroma_data"

    # 上传
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB

    # Agent
    MAX_TOOL_CALLS: int = 5
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50

    class Config:
        env_file = ".env"
```

---

## 十四、错误处理

### 14.1 错误码定义

| 错误码 | HTTP 状态码 | 说明 |
|--------|-----------|------|
| INVALID_REQUEST | 400 | 请求参数错误 |
| FILE_TOO_LARGE | 400 | 文件超过 50MB 限制 |
| UNSUPPORTED_FILE_TYPE | 400 | 不支持的文件格式 |
| SESSION_NOT_FOUND | 404 | 会话不存在 |
| DOCUMENT_NOT_FOUND | 404 | 文档不存在 |
| LLM_API_ERROR | 502 | DeepSeek API 调用失败 |
| TOOL_EXECUTION_ERROR | 502 | 工具执行失败 |
| VECTORSTORE_ERROR | 500 | ChromaDB 操作失败 |
| DATABASE_ERROR | 500 | MySQL 操作失败 |

### 14.2 SSE 错误事件

```
event: error
data: {"code": "LLM_API_ERROR", "message": "DeepSeek API 调用超时，请稍后重试"}
```

### 14.3 Agent 容错

- 工具调用失败时，将错误信息作为 Observation 返回 Agent，让 Agent 自行决定重试或换工具
- 达到 `max_tool_calls` 上限时强制终止循环，基于已有信息生成回答
- LLM API 超时返回友好错误提示

---

## 十五、开发环境配置

### 15.1 环境变量（.env）

```env
DEEPSEEK_API_KEY=sk-xxxx
TAVILY_API_KEY=tvly-xxxx
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=xxxx
MYSQL_DATABASE=ai_assistant
```

### 15.2 启动顺序

```bash
# 1. 后端
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# 2. 前端
cd frontend
npm install
npm run dev
```

---

## 十六、技术约束与注意事项

1. **DeepSeek API 兼容性**：DeepSeek API 兼容 OpenAI 格式，LangChain 可直接用 `ChatOpenAI` 配合 `base_url` 调用
2. **Embedding 维度**：DeepSeek Embedding 输出 1536 维向量，ChromaDB 自动适配
3. **SSE 限制**：EventSource 不支持 POST，需用 fetch + ReadableStream 实现
4. **MySQL 安全**：db_tool 使用 LLM 生成 SQL 后，仅允许 SELECT 查询，禁止 INSERT/UPDATE/DELETE/DROP
5. **文件存储**：上传文件存入 `./uploads/` 目录，ChromaDB 存入 `./chroma_data/` 目录
6. **会话上下文**：LangGraph 使用 MessagesState 管理对话历史，消息过长时需截断策略

