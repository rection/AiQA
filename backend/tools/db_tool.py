import re
from sqlalchemy import text
from database.session import engine
from langchain_openai import ChatOpenAI
from config import settings


def _generate_sql(natural_language: str) -> str:
    """用 LLM 将自然语言转为 SQL。"""
    llm = ChatOpenAI(
        model=settings.DEEPSEEK_MODEL,
        api_key=settings.DEEPSEEK_API_KEY,
        base_url=settings.DEEPSEEK_BASE_URL,
        temperature=0,
    )

    prompt = f"""你是一个 SQL 专家。根据用户的自然语言描述，生成对应的 MySQL SELECT 查询语句。

规则：
1. 只生成 SELECT 查询，禁止 INSERT/UPDATE/DELETE/DROP/ALTER/TRUNCATE
2. 只输出 SQL 语句，不要解释
3. 如果信息不足，生成最合理的查询

用户描述：{natural_language}

SQL："""

    response = llm.invoke(prompt)
    sql = response.content.strip()

    # 去掉可能的 markdown 代码块包裹
    sql = re.sub(r"^```sql\s*", "", sql)
    sql = re.sub(r"\s*```$", "", sql)

    # 安全检查：只允许 SELECT
    sql_upper = sql.upper().strip()
    dangerous_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE"]
    for kw in dangerous_keywords:
        if kw in sql_upper and not sql_upper.startswith("SELECT"):
            raise ValueError(f"SQL 包含危险操作: {kw}")

    return sql


def query(natural_language: str) -> str:
    """将自然语言转换为 SQL 并执行查询。"""
    sql = _generate_sql(natural_language)

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        columns = list(result.keys())

    if not rows:
        return f"执行 SQL：{sql}\n查询结果：无数据。"

    header = " | ".join(columns)
    separator = " | ".join(["---"] * len(columns))
    data_rows = []
    for row in rows[:50]:
        data_rows.append(" | ".join(str(v) for v in row))

    table = f"{header}\n{separator}\n" + "\n".join(data_rows)
    return f"执行的 SQL：\n```sql\n{sql}\n```\n\n查询结果（共 {len(rows)} 行）：\n{table}"
