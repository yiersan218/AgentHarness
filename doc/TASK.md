# AgentHarness 全栈 Agent Platform 研发计划

> 文档状态：执行基线  
> 当前版本：0.1.0  
> 目标版本：1.0.0  
> 计划范围：Agent Harness、API 服务、Web 前端、CLI/TUI、单机与生产部署  
> 更新日期：2026-08-27

## 1. 文档目标

本文用于指导 AgentHarness 从当前最小聊天程序，逐步开发为一个完整的全栈 Agent Platform。

最终系统需要同时具备：

- 可独立嵌入其他 Python 应用的 Agent Harness。
- 可供浏览器和第三方客户端调用的 API 服务。
- 支持多线程、多运行状态和实时事件的 Web 前端。
- 可配置的模型、工具、中间件和 Agent。
- 自定义 Agent、SOUL、文件、视觉、Skills、MCP、子 Agent 和记忆。
- 并发控制、取消、重新生成、自动目标推进和故障恢复。
- 安全、审计、Tracing、Token Usage 和生产部署能力。

本计划采用 P0～P16 的增量开发方式。每个阶段都必须同时交付后端能力、API 契约、对应前端交互和自动化测试，禁止把前端集中拖到最后补做。

## 2. 当前状态

### 2.1 已完成

- [x] Python 3.12+ 项目。
- [x] uv 依赖管理。
- [x] OpenAI 兼容模型配置。
- [x] 单节点 LangGraph。
- [x] 命令行多轮对话。
- [x] 基础离线测试。
- [x] 可执行 agent-harness 命令。

### 2.2 当前调用链

    CLI
      ↓
    build_agent
      ↓
    StateGraph(MessagesState)
      ↓
    ChatOpenAI

### 2.3 当前缺失

- 工具调用循环。
- Agent 工厂与扩展状态。
- 自定义 Agent 和 SOUL。
- 中间件体系。
- Streaming 和结构化事件。
- API 服务和 Web 前端。
- 线程、运行、事件和数据库。
- 并发、取消、恢复和重新生成。
- 沙盒、上传、Artifact、Workspace 和视觉。
- Skills、Skill Review、MCP、子 Agent 和记忆。
- 搜索、网页读取和引用。
- 授权、安全、审计和 Tracing。
- 生产部署和稳定 SDK。

## 3. 产品定位

AgentHarness 的 1.0 定位是：

> 一个支持自定义 Agent、工具执行、文件与视觉、多任务协作、长期记忆和实时 Web 交互的全栈 Agent Platform，同时提供可嵌入的 Python Harness。

### 3.1 目标用户

- 使用 Python 构建 Agent 应用的开发者。
- 需要部署私有 Agent 工作台的团队。
- 需要自定义 Agent、Skills、MCP 和工具的高级用户。
- 需要观察 Agent 运行过程、文件产物和子任务的 Web 用户。

### 3.2 1.0 核心能力

- 多模型配置。
- 多 Agent 与 SOUL。
- 工具调用和中间件。
- 流式对话。
- 线程和运行持久化。
- 本地沙盒。
- 文件上传和文档处理。
- Artifact 和 Workspace Changes。
- 图片理解。
- 并发运行策略。
- Cancel、Rollback、Regenerate 和 Edit-Regenerate。
- 自动 Goal Continuation。
- Skills 和 Skill Review。
- Web Search、Web Fetch 和引用。
- MCP。
- 子 Agent。
- 长期记忆。
- 授权、Guardrail 和 Secret 隔离。
- LangSmith、Langfuse、Monocle 可观测性接入。
- Web 管理界面。
- CLI/TUI。
- SQLite 默认部署，PostgreSQL/Redis 生产部署。

## 4. 系统架构

### 4.1 分层

    Web Frontend
        ↓ HTTP / SSE
    API Application
        ↓
    AgentHarnessClient / RunManager
        ↓
    Agent Factory + Middleware Chain
        ↓
    Model ← Agent Graph → Tool Registry
                           ├─ Built-in Tools
                           ├─ Sandbox Tools
                           ├─ Search / Fetch
                           ├─ Skill Tools
                           ├─ MCP Tools
                           └─ Subagent Tool
        ↓
    Runtime Context + ThreadState
        ↓
    Checkpointer / Store / Event Store
        ↓
    Memory / SQLite / PostgreSQL / Redis

### 4.2 依赖规则

- frontend 只通过公开 API 和 SSE 协议访问后端。
- API Application 可以导入 agent_harness。
- agent_harness 不得导入 API Application 或 frontend。
- CLI、TUI 和 API 必须复用 AgentHarnessClient。
- 前端不得直接持有模型 API Key。
- 数据库、沙盒和外部服务必须通过 Protocol 或 Provider 抽象访问。

### 4.3 推荐目录

    AgentHarness/
    ├── src/
    │   └── agent_harness/
    │       ├── agents/
    │       │   ├── factory.py
    │       │   ├── features.py
    │       │   ├── thread_state.py
    │       │   ├── lead_agent/
    │       │   └── middlewares/
    │       ├── client.py
    │       ├── config/
    │       ├── models/
    │       ├── tools/
    │       ├── runtime/
    │       │   ├── runs/
    │       │   ├── events/
    │       │   ├── checkpointer/
    │       │   ├── store/
    │       │   └── stream_bridge/
    │       ├── persistence/
    │       ├── sandbox/
    │       ├── uploads/
    │       ├── artifacts/
    │       ├── workspace_changes/
    │       ├── skills/
    │       ├── skill_review/
    │       ├── mcp/
    │       ├── subagents/
    │       ├── memory/
    │       ├── search/
    │       ├── authz/
    │       ├── guardrails/
    │       ├── tracing/
    │       ├── extensions/
    │       ├── tui/
    │       └── utils/
    ├── apps/
    │   └── api/
    │       ├── app.py
    │       ├── dependencies.py
    │       ├── schemas/
    │       ├── routers/
    │       └── services/
    ├── frontend/
    │   ├── app/
    │   ├── components/
    │   ├── features/
    │   ├── hooks/
    │   ├── lib/
    │   └── tests/
    ├── contracts/
    ├── doc/
    │   └── TASK.md
    ├── examples/
    ├── tests/
    ├── config.example.yaml
    ├── extensions_config.example.json
    ├── docker-compose.yml
    ├── AGENTS.md
    └── README.md

## 5. 前后端协同原则

### 5.1 API First

每项可视化功能必须先定义协议：

- 请求模型。
- 响应模型。
- 错误码。
- SSE 事件。
- 状态迁移。
- 权限要求。
- 幂等和重试语义。

前端不能通过解析自然语言判断运行状态。

### 5.2 前端阶段性交付

每个 P 阶段至少交付以下一种前端结果：

- 新页面。
- 新组件。
- 新状态卡片。
- 新配置面板。
- 新错误恢复流程。
- 对已有页面的正式 API 接入。

### 5.3 统一状态来源

- 服务端 RunRecord 是运行状态来源。
- Checkpointer 是 Agent 状态来源。
- EventStore 是可回放事件来源。
- 前端只维护这些状态的客户端投影。
- 页面刷新后必须能从 API 恢复，而不是依赖浏览器内存。

### 5.4 Progressive Enhancement

- API 不依赖前端存在。
- CLI/TUI 不依赖浏览器。
- JavaScript 不可用时，API 和 CLI 仍然可用。
- 前端实时连接失败时允许轮询恢复。

## 6. 核心协议

### 6.1 标识符

- user_id：数据所有者。
- agent_id：Agent 定义。
- thread_id：对话线程。
- run_id：一次 Agent 运行。
- message_id：消息。
- tool_call_id：工具调用关联。
- artifact_id：产物。
- task_id：子 Agent 任务。
- trace_id：观测关联。

这些 ID 不能互相替代。

### 6.2 RunStatus

    pending
    queued
    running
    waiting_for_input
    finalizing
    completed
    failed
    cancelled
    interrupted
    timed_out

### 6.3 StopReason

    completed
    user_cancelled
    interrupted_by_new_run
    rollback_requested
    token_capped
    turn_capped
    loop_capped
    model_length_capped
    safety_blocked
    tool_failure
    model_failure
    timeout

### 6.4 SSE 事件

    run.started
    run.status
    message.started
    message.delta
    message.completed
    tool.started
    tool.progress
    tool.completed
    tool.failed
    artifact.created
    workspace.changed
    clarification.requested
    goal.updated
    task.started
    task.progress
    task.completed
    task.failed
    usage.updated
    run.completed
    run.failed
    run.cancelled

所有事件必须：

- 包含 version。
- 包含 run_id。
- 需要时包含 thread_id、message_id、tool_call_id 或 task_id。
- 可 JSON 序列化。
- 支持 EventStore 回放。
- 不包含 Secret。

## 7. 里程碑总览

| 阶段 | 建议版本 | 后端重点 | 前端重点 | 粗略工作量 |
| --- | --- | --- | --- | --- |
| P0 | 0.1.x | 工程和 API 骨架 | Web 工程和设计系统 | 1 周 |
| P1 | 0.2.0 | 配置与模型工厂 | 模型设置页 | 1～2 周 |
| P2 | 0.3.0 | Agent 工厂、自定义 Agent、SOUL | Agent 管理页 | 2～3 周 |
| P3 | 0.4.0 | 工具和中间件 | 流式 Chat 与 Tool Card | 2～3 周 |
| P4 | 0.5.0 | Client、线程、运行、Streaming | 会话列表与恢复 | 3～4 周 |
| P5 | 0.6.0 | Local Sandbox | 文件与命令执行展示 | 2～3 周 |
| P6 | 0.7.0 | 上传、Artifact、Workspace、视觉 | 文件与 Artifact Workspace | 3～5 周 |
| P7 | 0.8.0 | 并发、Regenerate、自动 Goal | 运行控制与 Goal 面板 | 4～6 周 |
| P8 | 0.9.0 | 上下文、Todo、Human Input | Todo 与表单交互 | 2～4 周 |
| P9 | 0.10.0 | Skills 与 Skill Review | Skills 管理和评审报告 | 4～6 周 |
| P10 | 0.11.0 | Search、Fetch、MCP | 引用卡片和 MCP 设置 | 3～5 周 |
| P11 | 0.12.0 | 子 Agent | 子任务时间线 | 3～5 周 |
| P12 | 0.13.0 | 长期记忆 | Memory 管理页 | 3～5 周 |
| P13 | 0.14.0 | Auth、Guardrail、Tracing | 登录、审计和 Usage | 3～5 周 |
| P14 | 0.15.0 | Extensions、远程 Sandbox | 扩展和 Sandbox 状态页 | 4～6 周 |
| P15 | 0.16.0 | PostgreSQL、Redis、多实例 | 运维状态和故障恢复 | 4～8 周 |
| P16 | 1.0.0 | 稳定 SDK、TUI、发布 | UX 收尾和完整 E2E | 2～4 周 |

## 8. 分阶段详细计划

## P0：工程基础、API 骨架和前端骨架

### 目标

建立可以长期演进的全栈工程结构，同时保持当前 CLI 可用。

### Harness

- [ ] 调整测试目录为 unit、contract、integration、live。
- [ ] 引入 Ruff。
- [ ] 选择 Pyright 或 mypy。
- [ ] 定义公共模块和私有模块约定。
- [ ] 增加 CHANGELOG。
- [ ] 增加基础许可证文件。
- [ ] 保持当前 build_agent、CLI 和测试通过。

### API

- [ ] 创建 FastAPI Application。
- [ ] 增加 /health。
- [ ] 增加统一错误响应。
- [ ] 增加 Request ID。
- [ ] 增加 CORS 开发配置。
- [ ] API 层只能导入 agent_harness 公共 API。

### Frontend

- [ ] 创建 Next.js、TypeScript 前端。
- [ ] 使用 pnpm 管理依赖。
- [ ] 建立 App Router。
- [ ] 建立颜色、字体、间距和圆角 Token。
- [ ] 建立 Button、Input、Dialog、Dropdown、Toast、Tabs、Card。
- [ ] 建立响应式主布局。
- [ ] 建立 Light/Dark Theme。
- [ ] 创建空 Chat 页面。
- [ ] 创建 API Client。
- [ ] 显示后端健康状态。

### 工程

- [ ] 根命令同时启动 API 和 Frontend。
- [ ] CI 执行 Python 和前端检查。
- [ ] Python wheel 构建。
- [ ] Frontend production build。
- [ ] 添加基础 Dockerfile。

### 验收

- 一条命令启动 API 和 Web。
- Chat 空页面能够显示后端在线状态。
- CLI 仍能运行。
- Python 测试、前端测试和构建全部通过。

## P1：配置、模型工厂和模型设置页

### 目标

支持通过配置管理多个模型，并让用户在 Web 中查看和选择模型。

### Harness

- [ ] 使用 Pydantic 定义 AppConfig。
- [ ] 定义 ModelConfig。
- [ ] 支持 config.yaml。
- [ ] 支持环境变量引用 Secret。
- [ ] 实现 resolve_variable 和 resolve_class。
- [ ] 将模型构造移入 models/factory.py。
- [ ] 定义 supports_tools、supports_vision、supports_thinking。
- [ ] 支持 timeout、max_tokens、temperature、base_url。
- [ ] 支持运行级 model_name 选择。
- [ ] 模型构造错误提供明确诊断。
- [ ] 配置日志和 repr 脱敏。

### API

- [ ] GET /api/models。
- [ ] GET /api/models/{name}。
- [ ] GET /api/config/features。
- [ ] 配置写入初期仅允许本地 Operator，不向普通用户开放。

### Frontend

- [ ] 模型设置页。
- [ ] 模型选择器。
- [ ] 展示模型能力标签。
- [ ] 展示配置缺失和连接错误。
- [ ] Chat Header 显示当前模型。
- [ ] 模型切换时明确作用于下一次运行。

### 测试与验收

- [ ] 配置优先级测试。
- [ ] Secret 脱敏测试。
- [ ] Fake Model 注入测试。
- [ ] 模型列表契约测试。
- [ ] 设置页组件测试。
- 至少配置两个模型并在 Chat 中切换。

## P2：Agent 工厂、自定义 Agent 和 SOUL

### 目标

支持创建多个有独立身份、行为和运行配置的 Agent。

### Harness：Agent Core

- [ ] 创建 create_agent_harness 纯参数工厂。
- [ ] build_agent 保留为兼容入口。
- [ ] 定义 RuntimeFeatures。
- [ ] 定义 ThreadState 和 Reducer。
- [ ] 支持 model、tools、middleware、state_schema、checkpointer。
- [ ] 支持同步和异步调用。
- [ ] 定义 AgentConfig。
- [ ] 定义 AgentDefinition。

### Harness：Agent Storage

- [ ] 定义 AgentStorage Protocol。
- [ ] 实现 FileAgentStorage。
- [ ] 为后续 SQLAgentStorage 预留接口。
- [ ] 按 user_id 隔离。
- [ ] Agent 名称规范化和冲突检查。
- [ ] Agent 配置原子写入。
- [ ] SOUL 原子写入。
- [ ] Agent Definition revision。
- [ ] 乐观并发更新。
- [ ] 列表、读取、创建、更新、删除。

### Harness：SOUL 与自我更新

- [ ] 每个 Agent 支持 SOUL.md。
- [ ] SOUL 作为静态 Agent 身份提示的一部分。
- [ ] 配置支持模型、Tools、Skills、Memory 和 Subagent 策略。
- [ ] setup_agent 工具。
- [ ] update_agent 工具。
- [ ] Bootstrap Agent 创建流程。
- [ ] update_agent 只允许更新当前 Agent。
- [ ] 自我更新在下一次运行生效。
- [ ] 禁止空 SOUL 覆盖。
- [ ] 不可信入口禁止 Agent 自我更新。

### API

- [ ] GET /api/agents。
- [ ] GET /api/agents/{agent_id}。
- [ ] POST /api/agents。
- [ ] PATCH /api/agents/{agent_id}。
- [ ] DELETE /api/agents/{agent_id}。
- [ ] POST /api/agents/bootstrap。
- [ ] 并发更新使用 If-Match 或 revision。

### Frontend

- [ ] Agent 列表页。
- [ ] Agent 创建向导。
- [ ] Agent 编辑页。
- [ ] SOUL Markdown 编辑器。
- [ ] 模型、Tools、Skills 开关。
- [ ] Agent 复制。
- [ ] 删除确认。
- [ ] Chat 页 Agent 切换器。
- [ ] Agent 头像、名称和描述展示。
- [ ] 未保存修改提示。
- [ ] Revision 冲突提示和重新加载。

### 验收

- 两个用户的 Agent 不互相可见。
- 两个 Agent 使用不同 SOUL 时行为提示不同。
- Agent 可以创建并持久化自身更新。
- 非当前 Agent 不能被 update_agent 修改。
- 页面刷新后 Agent 配置仍存在。
- FileAgentStorage 通过完整契约测试。

## P3：工具系统、中间件和流式 Chat

### 目标

建立工具调用闭环和统一中间件链，让前端实时展示模型与工具状态。

### Harness：Tools

- [ ] Tool Registry。
- [ ] 工具分组、启用和禁用。
- [ ] 代码注册和配置注册。
- [ ] 同步和异步工具兼容。
- [ ] ToolResult 标准协议。
- [ ] Artifact 引用字段。
- [ ] calculator 示例工具。
- [ ] 工具名称冲突检查。

### Harness：Middleware

- [ ] InputSanitizationMiddleware。
- [ ] DanglingToolCallMiddleware。
- [ ] LLMErrorHandlingMiddleware。
- [ ] ToolErrorHandlingMiddleware。
- [ ] ToolOutputBudgetMiddleware。
- [ ] ToolResultSanitizationMiddleware。
- [ ] SystemMessageCoalescingMiddleware。
- [ ] LoopDetectionMiddleware。
- [ ] TokenBudgetMiddleware。
- [ ] TerminalResponseMiddleware。
- [ ] 集中组装并锁定顺序。

### API

- [ ] POST /api/chat/stream 作为早期流式入口。
- [ ] 使用 SSE 输出 message 和 tool 事件。
- [ ] 客户端断开时取消未完成请求。
- [ ] 统一模型和工具异常。

### Frontend

- [ ] 正式 Chat 页面。
- [ ] 用户消息和 Assistant 消息。
- [ ] Token 流式渲染。
- [ ] Tool Call Card。
- [ ] Tool Running、Success、Failed 状态。
- [ ] 可展开工具参数和结果。
- [ ] Stop 按钮。
- [ ] Retry 按钮。
- [ ] 连接失败提示。
- [ ] 断线重连基础逻辑。
- [ ] 自动滚动和手动滚动保护。

### 验收

- Fake Model 能完成 tool_call → result → final answer。
- 前端不会重复显示同一 Tool Call。
- 大输出不会导致页面冻结。
- Tool 异常不会直接结束整个服务。
- 中间件顺序有回归测试。

## P4：Embedded Client、Thread、Run、Streaming 和持久化

### 目标

建立正式运行生命周期，使浏览器刷新和进程重启后仍能恢复线程。

### Harness

- [ ] 创建 AgentHarnessClient。
- [ ] chat 和 stream。
- [ ] 定义 Runtime Context。
- [ ] 定义 StreamEvent。
- [ ] values、messages、custom、end。
- [ ] 增量消息按 message_id 重建。
- [ ] Tool Event 去重。
- [ ] Token Usage 去重。
- [ ] 支持 reset_agent。
- [ ] InMemorySaver。
- [ ] SQLite Checkpointer。
- [ ] ThreadMeta。
- [ ] RunRecord。
- [ ] RunEvent。
- [ ] EventStore Protocol。
- [ ] MemoryEventStore。
- [ ] SQLiteEventStore。
- [ ] RunManager 基础版本。

### API

- [ ] POST /api/threads。
- [ ] GET /api/threads。
- [ ] GET /api/threads/{thread_id}。
- [ ] DELETE /api/threads/{thread_id}。
- [ ] POST /api/threads/{thread_id}/runs。
- [ ] GET /api/threads/{thread_id}/runs。
- [ ] GET /api/runs/{run_id}。
- [ ] GET /api/runs/{run_id}/events。
- [ ] GET /api/runs/{run_id}/stream。

### Frontend

- [ ] Thread Sidebar。
- [ ] 新建、切换、重命名、删除 Thread。
- [ ] 历史消息恢复。
- [ ] Run Status Banner。
- [ ] 页面刷新后恢复运行。
- [ ] SSE 断线后使用 after_seq 补事件。
- [ ] 当前 Agent 和模型绑定到 Thread UI。
- [ ] 空状态和首次使用引导。

### 验收

- 重启后可以继续旧线程。
- chat 最终结果等于 stream 增量重建结果。
- Event seq 单调递增。
- 页面刷新不会丢失已完成消息。
- CLI 和 API 使用相同 AgentHarnessClient。

## P5：Local Sandbox 和文件执行

### 目标

为 Agent 提供线程隔离的文件与命令执行能力。

### Harness

- [ ] Sandbox Protocol。
- [ ] SandboxProvider Protocol。
- [ ] LocalSandboxProvider。
- [ ] user_id/thread_id 隔离目录。
- [ ] workspace、uploads、outputs。
- [ ] /mnt/user-data 虚拟路径。
- [ ] execute_command。
- [ ] read_file。
- [ ] write_file。
- [ ] str_replace。
- [ ] list_dir、glob、grep。
- [ ] 命令超时。
- [ ] 输出上限。
- [ ] 路径越界和符号链接保护。
- [ ] Secret 环境变量清理。
- [ ] 请求级环境变量注入。
- [ ] SandboxMiddleware。
- [ ] SandboxAuditMiddleware。
- [ ] ReadBeforeWriteMiddleware。
- [ ] 同一路径并发写锁。

### API

- [ ] GET /api/threads/{thread_id}/workspace。
- [ ] GET /api/threads/{thread_id}/workspace/files。
- [ ] GET /api/threads/{thread_id}/workspace/file。
- [ ] 文件接口必须验证 owner 和路径。

### Frontend

- [ ] Workspace 文件树。
- [ ] 文本文件预览。
- [ ] 代码高亮。
- [ ] Tool Card 展示命令、cwd、exit code 和耗时。
- [ ] 输出过长时折叠。
- [ ] 危险操作显示审计标记。

### 验收

- 两个线程无法读取彼此文件。
- 路径穿越和符号链接逃逸测试通过。
- 子进程看不到宿主模型 API Key。
- 超时命令可以回收。
- LocalSandbox 限制在文档中明确。

## P6：上传、Artifact、Workspace Changes 和视觉

### 目标

让用户可以向 Agent 提供文件和图片，并可靠获得运行产物。

### Harness：上传

- [ ] UploadService。
- [ ] 多文件上传。
- [ ] 文件名规范化。
- [ ] 同名文件自动编号。
- [ ] 大小和数量限制。
- [ ] 分块或流式写入。
- [ ] 临时文件完成后原子替换。
- [ ] 上传失败保持请求原子性。
- [ ] 上传列表和删除。
- [ ] 将上传文件注入当前线程上下文。
- [ ] PDF、Word、PPT、Excel 文本转换。
- [ ] 转换失败不损坏原始上传。

### Harness：Artifact

- [ ] Artifact 数据模型。
- [ ] present_files。
- [ ] MIME 检测。
- [ ] Artifact ID 和虚拟路径。
- [ ] Artifact 列表、读取和下载。
- [ ] 输出文件只允许来自 outputs。
- [ ] Tool 大输出可以外置为 Artifact。

### Harness：Workspace Changes

- [ ] 运行前 Snapshot。
- [ ] 运行后 Snapshot。
- [ ] 新增、修改、删除文件 Diff。
- [ ] 排除 .git、node_modules、内部临时目录。
- [ ] workspace.changed 事件。
- [ ] 运行记录保存 Workspace Changes。
- [ ] 输出验证失败时提供明确诊断。

### Harness：视觉

- [ ] view_image 工具。
- [ ] 图片格式和大小验证。
- [ ] Vision Middleware。
- [ ] 只有 supports_vision 模型获得图片内容。
- [ ] 图片作为隐藏多模态消息注入。
- [ ] 模型调用后清理 Base64 Payload。
- [ ] Checkpoint 不长期保存图片 Base64。
- [ ] 图片访问遵守 user/thread 隔离。

### API

- [ ] POST /api/threads/{thread_id}/uploads。
- [ ] GET /api/threads/{thread_id}/uploads。
- [ ] DELETE /api/threads/{thread_id}/uploads/{name}。
- [ ] GET /api/threads/{thread_id}/artifacts。
- [ ] GET /api/artifacts/{artifact_id}。
- [ ] GET /api/runs/{run_id}/workspace-changes。

### Frontend

- [ ] 拖拽上传。
- [ ] 上传进度。
- [ ] 文件 Chip。
- [ ] 文档转换状态。
- [ ] 图片缩略图。
- [ ] Artifact Panel。
- [ ] 图片、文本、PDF 和代码预览。
- [ ] 下载按钮。
- [ ] Workspace Changes 文件 Diff。
- [ ] 消息和 Artifact 关联。
- [ ] 上传错误的局部重试。

### 验收

- 多文件上传、同名、失败回滚测试通过。
- 文档转换测试使用本地 Fixture。
- 非视觉模型不会收到图片 Payload。
- 图片 Base64 不保留在最终 Checkpoint。
- Artifact 不能越权读取。
- 页面刷新后 Artifact 和 Workspace Changes 可恢复。

## P7：并发处理、Regenerate 和自动 Goal

### 目标

建立可解释、可恢复的并发运行机制，并支持重新生成和目标自动推进。

### Harness：并发

- [ ] 同线程活动运行约束。
- [ ] multitask_strategy=reject。
- [ ] multitask_strategy=interrupt。
- [ ] multitask_strategy=rollback。
- [ ] 不同线程允许并行运行。
- [ ] 进程级最大并发运行数。
- [ ] 每用户最大并发运行数。
- [ ] 等待队列。
- [ ] Run Cancellation。
- [ ] Finalization Barrier。
- [ ] 同线程 Checkpoint 写锁。
- [ ] 并发标题、事件和状态写入保护。
- [ ] Graceful Shutdown 等待或中断活动运行。
- [ ] Run Status 状态机不可逆校验。

### Harness：Regenerate

- [ ] Regenerate 最新可见 Assistant Message。
- [ ] 查找对应 Human Message。
- [ ] 解析父 Checkpoint。
- [ ] Regenerate Run Metadata。
- [ ] Edit-Regenerate。
- [ ] 失败时恢复原状态。
- [ ] 新结果成功后隐藏被替代结果。
- [ ] 防止选择错误分支。
- [ ] lineage cycle 和 dangling parent 检查。
- [ ] full checkpoint 模式先实现。

### Harness：Goal

- [ ] GoalState。
- [ ] objective、status、continuation_count、max_continuations。
- [ ] 设置、读取、清除 Goal。
- [ ] 每轮完成后 Goal Evaluator。
- [ ] 未完成时自动启动下一轮。
- [ ] 达到预算后停止。
- [ ] 等待用户输入时暂停自动继续。
- [ ] 取消运行时停止 continuation。
- [ ] Goal 事件持久化。
- [ ] Goal 评估模型可独立配置。

### API

- [ ] POST /api/runs/{run_id}/cancel。
- [ ] POST /api/threads/{thread_id}/runs/regenerate。
- [ ] POST /api/threads/{thread_id}/runs/edit-regenerate。
- [ ] GET /api/threads/{thread_id}/goal。
- [ ] PUT /api/threads/{thread_id}/goal。
- [ ] DELETE /api/threads/{thread_id}/goal。
- [ ] 409 表示并发策略冲突。

### Frontend

- [ ] Stop 当前运行。
- [ ] Reject 冲突提示。
- [ ] Interrupt 确认。
- [ ] Rollback 确认。
- [ ] 运行排队状态。
- [ ] Regenerate 按钮。
- [ ] Edit and Regenerate 编辑器。
- [ ] 被替代回答的 UI 状态。
- [ ] Goal Panel。
- [ ] Goal 进度和 continuation 次数。
- [ ] 自动继续时显示原因。
- [ ] Goal 暂停和清除。
- [ ] 多线程并行运行状态。

### 验收

- 同线程并发不会损坏 Checkpoint。
- reject、interrupt、rollback 有独立集成测试。
- 两个不同线程可以真实并发。
- Regenerate 不会选中 sibling branch。
- Edit-Regenerate 失败后原对话仍可用。
- Goal 达到完成、暂停或预算上限时正确停止。
- 页面刷新后排队、运行和 Goal 状态可恢复。

## P8：上下文治理、Todo、Title 和 Human Input

### 目标

支持长对话、规划任务和结构化用户确认。

### Harness

- [ ] DynamicContextMiddleware。
- [ ] SummarizationMiddleware。
- [ ] 消息数、Token 数和比例触发器。
- [ ] Tool Call/Tool Result 配对保留。
- [ ] summary_text 独立状态。
- [ ] DurableContextMiddleware。
- [ ] TodoListMiddleware。
- [ ] TitleMiddleware。
- [ ] TokenUsageMiddleware。
- [ ] ask_clarification。
- [ ] free_text。
- [ ] single choice。
- [ ] multi_select。
- [ ] form fields。
- [ ] Human Input 协议版本。
- [ ] waiting_for_input 状态。
- [ ] Answer 后 resume。
- [ ] 表单大小和字段限制。

### API

- [ ] POST /api/runs/{run_id}/input。
- [ ] POST /api/threads/{thread_id}/compact。
- [ ] PATCH /api/threads/{thread_id}/title。
- [ ] State API 返回 Todo 和 Usage。

### Frontend

- [ ] Todo Panel。
- [ ] Todo 实时状态。
- [ ] Human Input Card。
- [ ] 表单校验。
- [ ] 已回答卡片恢复。
- [ ] Context Compact 操作。
- [ ] Token Usage 展示。
- [ ] Thread Title 编辑。

### 验收

- 压缩后 Agent 仍能继续调用工具。
- Summary 数据不能升级为系统指令。
- Human Input 页面刷新后仍能回答。
- 重复提交同一回答保持幂等。
- Todo、Title 和 Usage 可持久化恢复。

## P9：Skills 和 Skill Review

### 目标

支持安装、启用、激活和审查可复用 Skill，同时确保 Review 不会激活目标 Skill。

### Harness：Skills

- [ ] Skill 数据模型。
- [ ] SKILL.md Frontmatter。
- [ ] name、description、license、allowed-tools、required-secrets。
- [ ] public、custom 和 integration 分类。
- [ ] 每用户启用状态。
- [ ] 同名覆盖规则。
- [ ] SkillCatalog。
- [ ] 完整发现模式。
- [ ] Deferred Discovery。
- [ ] describe_skill。
- [ ] /skill-name task。
- [ ] SkillActivationMiddleware。
- [ ] SkillToolPolicyMiddleware。
- [ ] 模型可见 Schema 和执行均检查策略。
- [ ] Skill Context 持久化引用。
- [ ] Sandbox Read-only Projection。
- [ ] .skill 安装、卸载和启停。

### Harness：Skill Review

- [ ] 只读 Package Snapshot。
- [ ] Frontmatter 验证。
- [ ] 文件、目录和资源清单。
- [ ] 路径、大小、数量和嵌套边界。
- [ ] 确定性静态扫描。
- [ ] Python、Shell 和配置风险规则。
- [ ] 找出缺失文档、测试和示例。
- [ ] 资源和 Eval 分析。
- [ ] Review Finding：severity、file、line、message、remediation。
- [ ] JSON Report。
- [ ] Markdown Report。
- [ ] CLI Review Command。
- [ ] review_skill_package 工具。
- [ ] Review 结果放入 Artifact。
- [ ] Review 不注册、启用或激活目标 Skill。
- [ ] Review 不执行目标脚本。
- [ ] Review 不访问网络。

### API

- [ ] GET /api/skills。
- [ ] GET /api/skills/{name}。
- [ ] POST /api/skills/install。
- [ ] PATCH /api/skills/{name}。
- [ ] DELETE /api/skills/{name}。
- [ ] POST /api/skills/review。
- [ ] GET /api/skill-reviews/{review_id}。

### Frontend

- [ ] Skills 列表页。
- [ ] 启用和禁用。
- [ ] Skill 详情和 Frontmatter。
- [ ] 上传安装 .skill。
- [ ] 安装前 Review。
- [ ] Review Summary。
- [ ] Findings 按严重级别筛选。
- [ ] 文件与行号定位。
- [ ] Markdown Report 预览和下载。
- [ ] 高危 Finding 阻止安装。
- [ ] Chat 中显示当前激活 Skill。

### 验收

- 禁用 Skill 不可激活。
- allowed-tools 不能通过直接调用或子 Agent 绕过。
- Secret 不进入消息、事件或 Trace。
- 恶意压缩包不能路径穿越。
- Review 目标不会被激活。
- Review 核心完全离线。
- 前端能解释阻止安装的具体 Finding。

## P10：Web Search、Web Fetch、引用和 MCP

### 目标

让 Agent 可以安全获取公开网页信息，并接入标准外部工具。

### Harness：Search

- [ ] WebSearchProvider Protocol。
- [ ] 至少一个无需复杂配置的搜索 Provider。
- [ ] 至少一个 API 型搜索 Provider 作为可选项。
- [ ] 标准 SearchResult：title、url、snippet、source。
- [ ] 结果数量和字符预算。
- [ ] 查询超时。
- [ ] Provider 错误标准化。
- [ ] web_search 工具。

### Harness：Fetch

- [ ] WebFetchProvider Protocol。
- [ ] httpx 下载。
- [ ] Redirect 限制。
- [ ] SSRF 检查。
- [ ] 私网和本地地址默认拒绝。
- [ ] Content-Type 检查。
- [ ] 下载大小上限。
- [ ] HTML 主体提取。
- [ ] HTML 转 Markdown。
- [ ] 标题、URL、抓取时间元数据。
- [ ] web_fetch 工具。
- [ ] 远程内容注入标签净化。

### Harness：引用

- [ ] Citation 数据模型。
- [ ] SearchResult 与消息引用关联。
- [ ] 最终回答保留 URL 和标题。
- [ ] 重复 URL 去重。
- [ ] 引用数据可持久化和回放。

### Harness：MCP

- [ ] MCP Server 配置。
- [ ] stdio、HTTP、SSE。
- [ ] 多服务器工具发现。
- [ ] 工具名称前缀。
- [ ] Lazy Initialization。
- [ ] 配置内容签名与缓存失效。
- [ ] user/thread 级 stdio session。
- [ ] 初始化和工具调用 Timeout。
- [ ] OAuth 和 Refresh。
- [ ] Tool Search 和 Deferred Schema。
- [ ] Routing Hint。
- [ ] MCP Path Translation。
- [ ] stdio Command Allowlist。
- [ ] MCP Result 标准化。

### API

- [ ] Search 和 Fetch 默认只作为 Agent Tool，不提供匿名代理接口。
- [ ] GET /api/mcp。
- [ ] PUT /api/mcp。
- [ ] PATCH /api/mcp/{server}/enabled。
- [ ] POST /api/mcp/{server}/test。

### Frontend

- [ ] Search Tool Card。
- [ ] Search Results List。
- [ ] Citation Chips。
- [ ] 引用 Hover Preview。
- [ ] Fetch 内容预览。
- [ ] 外部链接安全打开。
- [ ] MCP Server 设置页。
- [ ] Transport、状态和工具数量。
- [ ] Connection Test。
- [ ] OAuth 状态。
- [ ] Tool Search Promotion 状态。

### 验收

- Search 和 Fetch 在 Timeout 后释放资源。
- 私网 SSRF 测试通过。
- 超大网页不会进入模型上下文。
- 恶意网页不能伪造系统标签。
- 引用在刷新后仍存在。
- 一个 MCP Server 失败不影响其他 Server。

## P11：子 Agent 和前端子任务时间线

### 目标

支持受控委派和并行子任务，并让用户实时了解每个子任务。

### Harness

- [ ] SubagentSpec。
- [ ] SubagentRegistry。
- [ ] general-purpose 子 Agent。
- [ ] task 工具。
- [ ] SubagentExecutor。
- [ ] 独立临时状态。
- [ ] 不继承父 Checkpointer。
- [ ] 默认禁止嵌套 task。
- [ ] max_concurrent_subagents。
- [ ] max_total_subagents。
- [ ] timeout。
- [ ] max_turns。
- [ ] token budget。
- [ ] loop detection。
- [ ] started、running、completed、failed、timed_out。
- [ ] stop_reason。
- [ ] Step Capture。
- [ ] Step Event 持久化。
- [ ] Tool Output 截断。
- [ ] Token Usage 回传父运行。
- [ ] Delegation Ledger。
- [ ] 父运行取消时清理子任务。
- [ ] ContextVar 和 Callback 隔离。
- [ ] 父子 Trace 关联。

### API

- [ ] GET /api/runs/{run_id}/tasks。
- [ ] GET /api/tasks/{task_id}。
- [ ] GET /api/tasks/{task_id}/events。
- [ ] POST /api/tasks/{task_id}/cancel。
- [ ] 支持 after_seq 分页。

### Frontend

- [ ] Subtask Card。
- [ ] 状态、模型、耗时和 Usage。
- [ ] 展开步骤时间线。
- [ ] Tool Step。
- [ ] Partial Result。
- [ ] Stop Reason。
- [ ] 子任务取消。
- [ ] 多子任务并行布局。
- [ ] 页面刷新后回填步骤。

### 验收

- 并行子任务不会共享消息状态。
- 超出委派限制时明确提示。
- 子任务失败不丢失其他结果。
- 子任务取消后资源释放。
- 步骤分页不会因为运行事件过多丢失尾部。
- 父运行 Usage 不重复计算。

## P12：长期记忆和 Memory 管理页

### 目标

提供用户级和 Agent 级长期记忆，并允许用户查看、更正和删除。

### Harness

- [ ] MemoryManager Protocol。
- [ ] NoopMemory。
- [ ] FileMemory。
- [ ] 用户摘要和 Agent 事实分离。
- [ ] Fact 数据模型。
- [ ] search、add、update、delete。
- [ ] user_id 隔离。
- [ ] agent_id 隔离。
- [ ] MemoryMiddleware。
- [ ] 只捕获真实用户输入和最终回答。
- [ ] Debounce Queue。
- [ ] Bounded Shutdown Flush。
- [ ] Dynamic Context Injection。
- [ ] 注入 Token Budget。
- [ ] SQLite FTS5 Retrieval。
- [ ] 原子事实写入。
- [ ] Revision 和冲突。
- [ ] 重复事实去重。
- [ ] Capacity Eviction。
- [ ] Staleness Review。
- [ ] Middleware Mode。
- [ ] Tool Mode。

### API

- [ ] GET /api/memory。
- [ ] GET /api/memory/facts。
- [ ] POST /api/memory/facts。
- [ ] PATCH /api/memory/facts/{id}。
- [ ] DELETE /api/memory/facts/{id}。
- [ ] POST /api/memory/search。
- [ ] POST /api/memory/reload。
- [ ] DELETE /api/memory。

### Frontend

- [ ] Memory Overview。
- [ ] 用户摘要。
- [ ] 按 Agent 查看 Facts。
- [ ] 搜索、筛选和排序。
- [ ] 创建、编辑和删除 Fact。
- [ ] Confidence 和时间展示。
- [ ] Memory 开关。
- [ ] 清空确认。
- [ ] 显示本次回答使用了哪些 Memory。

### 验收

- 用户和 Agent 之间严格隔离。
- Memory 抽取失败不影响主运行。
- 页面操作与 Agent Tool 使用同一存储契约。
- 被删除 Fact 不再被检索。
- 记忆内容不能伪装成系统指令。

## P13：授权、Guardrail、Tracing、审计和 Usage

### 目标

形成统一安全边界和完整可观测性。

### Harness：Authorization

- [ ] Principal。
- [ ] AuthorizationProvider。
- [ ] 构建阶段过滤模型可见工具。
- [ ] 执行阶段再次授权。
- [ ] Agent、Thread、Artifact、Memory 和 Skill Owner Check。
- [ ] 管理员能力。
- [ ] GuardrailProvider。
- [ ] fail-open/fail-closed 明确配置。
- [ ] Secret Context。
- [ ] Secret Redaction。
- [ ] 输入、远程工具内容和日志净化。

### Harness：Tracing

- [ ] trace_id ContextVar。
- [ ] 结构化日志。
- [ ] Graph Root Callback。
- [ ] LangSmith 可选接入。
- [ ] Langfuse 可选接入。
- [ ] Monocle 可选接入。
- [ ] thread_id、run_id、agent_id 和 user_id Metadata。
- [ ] 子 Agent Trace 关联。
- [ ] 系统模型调用观测。
- [ ] Token Usage 分类。
- [ ] Run Journal。
- [ ] Audit Event。
- [ ] 防止重复 Root Trace。
- [ ] Trace 数据脱敏。

### API

- [ ] 登录和会话基础。
- [ ] Role 和 Permission。
- [ ] GET /api/me。
- [ ] GET /api/usage。
- [ ] GET /api/audit-events。
- [ ] 管理接口和普通运行接口分离。
- [ ] CSRF 和 Origin 检查。
- [ ] Rate Limit。

### Frontend

- [ ] 登录页。
- [ ] 用户菜单。
- [ ] 权限不足页面。
- [ ] Usage Dashboard。
- [ ] 按模型、Agent 和时间查看 Token。
- [ ] Run Detail 展示 trace_id。
- [ ] 外部 Trace 链接。
- [ ] Audit Log 页面。
- [ ] 安全设置。

### 验收

- 未授权工具既不可见也不可执行。
- Secret 不出现在消息、事件、Checkpoint、Trace 或日志。
- 一次运行只产生一个根 Trace。
- 子 Agent Trace 可以关联父 Thread。
- Usage 不重复计算。
- 普通用户无法访问管理接口。

## P14：Extension、远程 Sandbox 和扩展管理

### 目标

支持第三方扩展和强隔离执行。

### Harness：Extensions

- [ ] 独立 Extension API。
- [ ] Registry Contract。
- [ ] Middleware Contribution。
- [ ] Task Lifecycle Hook。
- [ ] System Model Observer。
- [ ] Service Hook。
- [ ] 语义化中间件位置。
- [ ] 扩展失败隔离。
- [ ] 版本兼容检查。
- [ ] PEP 621 Entry Point。
- [ ] install、list、enable、disable、remove。
- [ ] 依赖更新事务。
- [ ] 本地源码快照。
- [ ] 扩展诊断。
- [ ] 扩展变更要求重启。

### Harness：Remote Sandbox

- [ ] RemoteSandboxProvider Protocol。
- [ ] 至少一个容器型 Provider。
- [ ] 创建、获取、释放和销毁。
- [ ] Readiness Probe。
- [ ] Workspace Mount。
- [ ] Skill Projection Mount。
- [ ] Upload Sync。
- [ ] Output Sync。
- [ ] Capacity Limit。
- [ ] Acquire Timeout。
- [ ] Idle Reaping。
- [ ] Remote Failure Classification。

### API

- [ ] GET /api/extensions。
- [ ] POST /api/extensions/install。
- [ ] PATCH /api/extensions/{name}。
- [ ] DELETE /api/extensions/{name}。
- [ ] GET /api/sandboxes。
- [ ] GET /api/sandboxes/{id}。
- [ ] DELETE /api/sandboxes/{id}。

### Frontend

- [ ] Extensions 管理页。
- [ ] 安装来源和信任警告。
- [ ] 版本、状态和诊断。
- [ ] Sandbox 状态页。
- [ ] Provider、Thread、创建时间、状态。
- [ ] 手动销毁。
- [ ] 容量和错误提示。

### 验收

- 可选扩展失败不阻止核心启动。
- Required 扩展失败会明确终止启动。
- 扩展异常不会重复执行下游模型或工具。
- 不健康 Sandbox 不会交给 Agent。
- Remote Sandbox 失败不会暴露宿主 Secret。

## P15：生产持久化、多实例、部署和运维前端

### 目标

支持 PostgreSQL、Redis、多实例运行和可观测部署。

### Backend

- [ ] SQLAlchemy 2。
- [ ] Alembic。
- [ ] PostgreSQL。
- [ ] Thread、Run、Event、Agent、Memory、Artifact Repository。
- [ ] Redis Stream Bridge。
- [ ] 多实例 Run Ownership。
- [ ] Heartbeat 和 Lease。
- [ ] 陈旧运行恢复。
- [ ] 跨实例最大并发。
- [ ] Remote Sandbox Ownership。
- [ ] Warm Pool。
- [ ] Orphan Reconciliation。
- [ ] Graceful Shutdown 和 Drain。
- [ ] Health、Readiness、Liveness。
- [ ] 数据库备份和恢复文档。
- [ ] Docker Compose。
- [ ] 生产环境配置校验。
- [ ] Delta Checkpoint 只在基准证明需要后实施。

### Frontend

- [ ] System Status 页面。
- [ ] API、DB、Redis、Sandbox Provider 状态。
- [ ] 当前活动运行数量。
- [ ] 队列长度。
- [ ] 失败运行列表。
- [ ] 运维诊断下载。
- [ ] 降级状态 Banner。
- [ ] 前端静态资源生产构建。

### 测试与验收

- [ ] 多实例竞争测试。
- [ ] Lease Expiry 测试。
- [ ] 进程崩溃恢复测试。
- [ ] PostgreSQL 集成测试。
- [ ] Redis 集成测试。
- [ ] Sandbox Ownership 故障注入。
- [ ] Compose 一键启动。
- 一个实例不能停止另一个实例正在执行的资源。

## P16：稳定 SDK、TUI、前端收尾和 1.0 发布

### 目标

冻结公共协议，完成完整 E2E 和用户体验收尾。

### SDK

- [ ] 明确 Public API。
- [ ] AgentHarnessClient API Reference。
- [ ] 同步和异步调用。
- [ ] chat、stream、threads、runs、agents、skills、memory、artifacts。
- [ ] 类型完整。
- [ ] 公共异常体系。
- [ ] SemVer 策略。
- [ ] StreamEvent v1。
- [ ] RunStatus v1。
- [ ] ToolResult v1。
- [ ] HumanInput v1。
- [ ] SubagentStatus v1。
- [ ] Extension API v1。

### CLI/TUI

- [ ] CLI chat。
- [ ] CLI config check。
- [ ] CLI doctor。
- [ ] CLI Skill Review。
- [ ] TUI 使用 AgentHarnessClient。
- [ ] TUI Thread 和 Agent 切换。
- [ ] TUI Tool、Task、Goal 和 Usage 展示。
- [ ] Headless JSON 模式。

### Frontend

- [ ] 全局导航和信息架构复核。
- [ ] Chat、Agents、Workspace、Skills、Memory、Settings 页面统一。
- [ ] Mobile 和 Desktop 响应式。
- [ ] Keyboard Navigation。
- [ ] Accessibility Audit。
- [ ] Loading、Empty、Error、Offline 状态统一。
- [ ] SSE 断线恢复。
- [ ] Error Boundary。
- [ ] 性能分析。
- [ ] 长消息和大量 Tool Card 虚拟化。
- [ ] 浏览器 E2E。
- [ ] 首次使用引导。
- [ ] About 和版本信息。

### 文档与示例

- [ ] Quick Start。
- [ ] Configuration。
- [ ] Architecture。
- [ ] API Reference。
- [ ] Security Model。
- [ ] Deployment。
- [ ] Troubleshooting。
- [ ] Upgrade Guide。
- [ ] 自定义 Agent 示例。
- [ ] Tool 示例。
- [ ] Middleware 示例。
- [ ] Skill 示例。
- [ ] MCP 示例。
- [ ] Subagent 示例。
- [ ] 前端开发指南。

### 1.0 验收

- [ ] 新环境可以一键安装和启动。
- [ ] SQLite 单机模式开箱即用。
- [ ] PostgreSQL/Redis 模式有完整部署说明。
- [ ] CLI、TUI、API 和 Web 共享同一 Harness。
- [ ] 自定义 Agent 与 SOUL 完整可用。
- [ ] 上传、Artifact、Workspace 和视觉完整可用。
- [ ] 并发、Regenerate 和自动 Goal 完整可用。
- [ ] Skills 和 Skill Review 完整可用。
- [ ] Search、Fetch、Citation 和 MCP 完整可用。
- [ ] Subagent 和 Memory 完整可用。
- [ ] Tracing 和 Usage 完整可用。
- [ ] 页面刷新不丢失持久状态。
- [ ] offline tests 不需要外部 API。
- [ ] live tests 必须显式启用。
- [ ] 公共协议全部有契约测试。
- [ ] wheel 和前端 production build 通过。

## 9. 选定功能落位表

| 功能 | 阶段 | 后端交付 | 前端交付 |
| --- | --- | --- | --- |
| 自定义 Agent | P2 | AgentFactory、AgentStorage、CRUD | Agent 管理页 |
| SOUL | P2 | SOUL 存储、Bootstrap、自我更新 | SOUL 编辑器 |
| 上传 | P6 | UploadService、文档转换 | 拖拽上传和进度 |
| Artifact | P6 | Artifact 协议和读取 | Artifact Panel |
| Workspace Changes | P6 | Snapshot 和 Diff | 文件变化视图 |
| 视觉 | P6 | view_image 和 Vision Middleware | 图片预览 |
| 并发处理 | P7 | RunManager 策略、锁和队列 | 运行控制和状态 |
| Regenerate | P7 | Regenerate、Edit-Regenerate、Lineage | 重新生成和编辑 |
| 自动 Goal | P7 | Goal Evaluator 和 Continuation | Goal Panel |
| Skill Review | P9 | Review Core 和 Tool | Review 报告页 |
| Tracing | P13 | LangSmith、Langfuse、Monocle | Trace 与 Usage |
| Web Search | P10 | Search Provider 和 Tool | Search Result Card |
| Web Fetch | P10 | 安全读取和正文提取 | Fetch Preview |
| 阶段性前端 | P0～P16 | API 契约和 SSE | 每阶段同步交付 |

## 10. 测试体系

### 10.1 Python Unit

- Config。
- Reducer。
- AgentStorage。
- Tool Registry。
- Middleware。
- Run State Machine。
- Sandbox Path。
- Upload Validation。
- Workspace Diff。
- Goal Evaluator。
- Skill Parser。
- Skill Review。
- Search/Fetch Security。
- Memory Logic。

### 10.2 Python Contract

- AgentHarnessClient。
- ModelProvider。
- SandboxProvider。
- Checkpointer。
- EventStore。
- AgentStorage。
- ArtifactStore。
- MemoryManager。
- SearchProvider。
- MCP。
- StreamEvent。
- RunStatus。
- SubagentStatus。
- Extension API。

### 10.3 Python Integration

- Fake Model Tool Loop。
- Client + SQLite。
- Run Concurrency。
- Cancel/Interrupt/Rollback。
- Regenerate。
- Goal Continuation。
- Upload + Document Conversion。
- Local Sandbox。
- Skill Install + Review。
- Mock Search/Fetch。
- Mock MCP Server。
- Subagent。
- Memory Queue。

### 10.4 Frontend

- Reducer Unit Tests。
- API Client Tests。
- SSE Parser Tests。
- Component Tests。
- Accessibility Tests。
- Mock Service Worker Integration。
- Playwright E2E。
- Refresh Recovery。
- Offline/Disconnect Recovery。

### 10.5 Live

- 真实模型。
- 真实 Search Provider。
- 真实 MCP。
- PostgreSQL。
- Redis。
- Remote Sandbox。
- Tracing Provider。

Live 测试默认不运行，必须明确声明可能产生费用和外部副作用。

## 11. 安全清单

- [ ] 所有资源按 user_id 做 Owner Check。
- [ ] Agent Self-update 只允许可信入口。
- [ ] 上传文件名、路径、大小和数量受限。
- [ ] 压缩包防路径穿越。
- [ ] Workspace 和 Artifact 防路径越界。
- [ ] URL 防 SSRF。
- [ ] Redirect 重新检查目标。
- [ ] Shell 不继承宿主 Secret。
- [ ] MCP stdio 仅允许可信 Operator 配置。
- [ ] Skill Secret 通过 Runtime Context 传递。
- [ ] Secret 不进入消息。
- [ ] Secret 不进入 Checkpoint。
- [ ] Secret 不进入 Event。
- [ ] Secret 不进入 Trace。
- [ ] Secret 不进入日志。
- [ ] 外部网页和 MCP 内容按不可信数据处理。
- [ ] 前端不保存模型 Key。
- [ ] 管理 API 有独立权限。
- [ ] CSRF、Origin 和 Rate Limit 生效。

## 12. 前端体验标准

- 所有异步操作都有 Loading、Success、Error。
- 所有危险操作都需要确认。
- 所有后台运行都能查看状态。
- 所有失败运行都提供可操作的下一步。
- 页面刷新后状态可恢复。
- Tool、Task、Goal、Artifact 使用稳定结构化协议。
- 不解析 Assistant 文本推断系统状态。
- 支持键盘操作。
- 颜色不是唯一状态表达。
- 支持窄屏。
- 长消息、长列表和大文件不会阻塞主线程。
- SSE 断线后可从 EventStore 补齐。

## 13. 质量门禁

每个阶段完成前：

- [ ] 后端行为有自动测试。
- [ ] API 有契约测试。
- [ ] 对应前端已交付。
- [ ] 前端组件有测试。
- [ ] 至少一条对应 E2E 用户路径。
- [ ] Python lint、format 和 type check 通过。
- [ ] Frontend lint、type check 和 build 通过。
- [ ] 外部调用有 Timeout。
- [ ] 后台任务有 Shutdown。
- [ ] 缓存有失效策略。
- [ ] 数据变更有数据库 Schema 处理。
- [ ] Secret 和权限影响已评估。
- [ ] README 和 AGENTS.md 已同步。
- [ ] doc/TASK.md 状态已更新。

## 14. 性能预算

- API Health：本地环境 P95 小于 100ms。
- 首个非模型 API 页面：本地环境 P95 小于 300ms。
- SSE 建连：本地环境 P95 小于 500ms。
- Tool Event 从后端到前端：正常网络下 P95 小于 500ms。
- 前端初始 JS Bundle 设定预算并持续监控。
- 消息列表超过 1,000 项时使用虚拟化或分段加载。
- Tool 大输出不直接进入消息 DOM。
- Artifact 采用流式下载。
- Checkpoint 性能优化必须先有正确性对照基准。
- 并发上限必须可配置并可观测。

## 15. 风险

| 风险 | 影响 | 处理 |
| --- | --- | --- |
| 前后端协议频繁变化 | 重复返工 | 先定义 versioned contract |
| 同线程并发写状态 | Checkpoint 损坏 | RunManager、锁和状态机 |
| Agent 自我更新越权 | 持久配置被篡改 | 当前 Agent 限制和可信入口 |
| 上传恶意文件 | 路径和资源风险 | 限额、原子写、转换隔离 |
| 图片 Payload 持久化 | 数据库膨胀和隐私风险 | 调用后清理，只保存引用 |
| Regenerate 选择错误分支 | 历史被错误替换 | Lineage 校验和失败回滚 |
| 自动 Goal 无限运行 | 费用失控 | Continuation、Token、Turn 预算 |
| Skill Review 执行目标代码 | 安全风险 | 完全只读和离线 |
| Search/Fetch SSRF | 内网暴露 | DNS/IP/Redirect 全链路检查 |
| 子 Agent 并发失控 | 资源耗尽 | 并发、总量、Token、Turn、Timeout |
| Tracing 泄漏数据 | 隐私风险 | Metadata 白名单和统一脱敏 |
| Frontend 依赖临时事件 | 刷新丢状态 | EventStore 回放和 API 恢复 |
| 多实例 Lease 错误 | 重复执行或误杀资源 | Fencing、Heartbeat、故障注入 |

## 16. 推荐开发节奏

### 第一阶段：可用全栈 Agent

完成 P0～P4：

- Web Chat。
- 模型设置。
- 自定义 Agent 和 SOUL。
- 工具调用。
- Thread 和 Run 持久化。

### 第二阶段：文件与高级运行

完成 P5～P8：

- Sandbox。
- 上传、Artifact、Workspace 和视觉。
- 并发、Regenerate 和自动 Goal。
- Todo、Summary 和 Human Input。

### 第三阶段：扩展能力

完成 P9～P12：

- Skills 和 Skill Review。
- Search、Fetch、Citation 和 MCP。
- 子 Agent。
- Memory。

### 第四阶段：生产化

完成 P13～P16：

- Security 和 Tracing。
- Extensions 和 Remote Sandbox。
- PostgreSQL、Redis 和多实例。
- SDK、TUI、前端收尾和 1.0。

## 17. 1.0 Definition of Done

- [ ] Harness 可以被第三方 Python 项目独立使用。
- [ ] API 和 Web 不改变 Harness 行为。
- [ ] 自定义 Agent、SOUL、Bootstrap 和 Self-update 可用。
- [ ] 多模型、Tools 和 Middleware 可配置。
- [ ] Thread、Run、Event 和 Checkpoint 可恢复。
- [ ] 并发策略、取消和 Graceful Shutdown 可用。
- [ ] Regenerate 和 Edit-Regenerate 可用。
- [ ] Goal 可以自动推进且有预算。
- [ ] Local 和 Remote Sandbox 可用。
- [ ] 上传、文档、Artifact、Workspace Changes 和视觉可用。
- [ ] Skills、Policy 和 Skill Review 可用。
- [ ] Search、Fetch、Citation 和 MCP 可用。
- [ ] Subagent 和 Memory 可用。
- [ ] Authorization、Guardrail、Audit 和 Secret Redaction 可用。
- [ ] LangSmith、Langfuse、Monocle 至少可以按配置接入。
- [ ] Web 覆盖主要管理与运行能力。
- [ ] 页面刷新和断线不会丢失已持久化状态。
- [ ] CLI、TUI、API、Web 共享同一 Client 和协议。
- [ ] SQLite 默认模式可用。
- [ ] PostgreSQL/Redis 生产模式可用。
- [ ] 核心测试默认不访问外部服务。
- [ ] 所有公共协议有版本和契约测试。
- [ ] 文档覆盖开发、使用、安全、部署和升级。

## 18. 状态约定

- [ ] 未开始。
- [~] 开发中。
- [x] 已完成且通过验收。
- [!] 阻塞，需要在任务下记录原因和解除条件。

完成阶段后必须同步：

- doc/TASK.md 状态。
- CHANGELOG。
- README。
- AGENTS.md。
- API Contract。
- 前端对应页面说明。
