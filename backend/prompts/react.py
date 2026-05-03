REACT_SYSTEM_SUFFIX = """

你拥有以下工具可以使用：

{tools_description}

当你需要使用工具时，请使用以下 JSON 格式调用：
```json
{{
  "tool": "工具名称",
  "input": "工具输入参数"
}}
```

当你不需要使用工具或已获取足够信息时，直接给出最终回答。
"""
