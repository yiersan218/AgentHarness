# AgentHarness

一个从 DeerFlow 核心思路中提炼出的最小 Agent 框架。项目只包含：

- 一个 OpenAI 兼容聊天模型
- 一个只有模型节点的 LangGraph 状态图
- 一个命令行多轮对话入口
- 少量离线单元测试

它不包含工具、沙盒、记忆持久化、数据库、MCP、子 Agent、HTTP API 或前端。

## 架构

```text
命令行输入 -> LangGraph(MessagesState) -> ChatOpenAI -> 命令行输出
```

对话历史只保存在当前 Python 进程中。退出程序后不会保留任何数据。

## 环境要求

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- 一个 OpenAI 或 OpenAI 兼容模型服务

## 运行

PowerShell：

```powershell
uv sync
$env:MODEL_NAME = "你的模型名称"
$env:OPENAI_API_KEY = "你的 API Key"
# 使用兼容服务时再设置：
# $env:OPENAI_BASE_URL = "https://你的服务地址/v1"
uv run agent-harness
```

输入 `exit` 或 `quit` 退出。

也可以不安装命令行脚本，直接运行：

```powershell
uv run python -m agent_harness
```

## 测试

```powershell
uv run pytest
```

测试使用本地假模型，不会访问网络，也不会消耗 API 额度。

## 目录

```text
AgentHarness/
├── src/agent_harness/
│   ├── agent.py       # 最小 LangGraph 图
│   ├── config.py      # 环境变量配置
│   └── cli.py         # 命令行入口
├── tests/
├── .env.example
└── pyproject.toml
```

后续需要工具、API、持久化等能力时，可以在这个最小闭环上逐项增加，而无需继承 DeerFlow 的复杂运行时。
