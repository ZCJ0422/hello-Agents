# Hello Agents：旅行助手

这是一个基于大语言模型的命令行旅行助手。它可以查询城市天气，并根据天气搜索适合游览的景点。

程序通过 Thought/Action 流程逐步完成请求：模型先决定调用哪个工具，程序执行工具并把结果交回模型，最后由模型生成答复。当前提供的工具有：

- `get_weather`：通过 wttr.in 查询天气。
- `get_attraction`：通过 Tavily 搜索景点建议。

## 环境要求

- Python 3.9 或更高版本
- [uv](https://docs.astral.sh/uv/)
- 一个兼容 OpenAI Chat Completions API 的模型服务
- Tavily API 密钥（需要使用景点搜索功能时）

## 配置密钥

在项目根目录复制配置模板：

```bash
cp .env.example .env
```

编辑 `.env`，填入自己的服务配置：

```dotenv
OPENAI_API_KEY=你的模型服务密钥
OPENAI_BASE_URL=https://你的服务商提供的地址/v1
OPENAI_MODEL=你的模型名称
TAVILY_API_KEY=你的Tavily密钥
```

`OPENAI_BASE_URL` 和 `OPENAI_MODEL` 应填写模型服务商提供的值。天气查询不需要额外密钥；景点搜索需要 `TAVILY_API_KEY`。

程序会在启动时读取项目根目录的 `.env`。也可以在终端中设置环境变量；如果同一变量同时出现在终端和 `.env` 中，终端变量优先。`.env` 已加入 `.gitignore`，不要把真实密钥提交到代码仓库。

## 运行

在项目根目录运行，并把要处理的问题作为参数传入：

```bash
uv run hello-agents "帮我查一下上海今天的天气，并推荐一个适合游览的景点"
```

不传参数时，会使用内置的北京天气示例：

```bash
uv run hello-agents
```

也可以直接运行兼容入口：

```bash
uv run python agent1.py "帮我查一下杭州今天的天气"
```

`uv run` 会根据项目配置准备运行环境和依赖。首次运行可能需要联网下载依赖。

## 项目结构

```text
src/hello_agents/
├── agent.py       # Agent 循环、Action 解析和工具调度
├── llm_client.py  # OpenAI 兼容模型客户端
├── main.py        # 配置加载和命令行入口
├── prompts.py     # Agent 系统提示词
└── tools.py       # 天气与景点搜索工具
```

根目录的 `agent1.py` 是兼容入口；新功能和主要实现放在 `src/hello_agents/` 中。
