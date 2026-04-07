# RAG-for-practice

轻量级 RAG（Retrieval-Augmented Generation）练习项目

功能概览
- 支持将本地 TXT 文件拆分并上传到 Chroma 向量数据库
- 使用向量检索 + 聊天模型进行问答（RAG）
- 兼容所有OPENAI格式的大模型(LLMs)以及嵌入模型(Embedding-models)
- 保存聊天历史到本地文件(JSON持久化存储)
- 提供 Streamlit 前端用于文件上传与对话（`client.py`）

安全与配置
- 推荐方式：使用 `uv` 管理依赖并通过环境变量或本地未跟踪文件 `configdata.py` 修改配置

快速启动（使用 `uv`）==推荐==
1. 创建并激活虚拟环境：

```powershell
uv venv
```

2. 使用 `uv` 安装依赖：

```powershell
uv sync
# 若需要额外包，可按需添加，例如: uv add tiktoken chromadb
```

3. 启动前端：

```powershell
streamlit run client.py
```

备用：使用 `requirements.txt`
```powershell
pip install -r requirements.txt
streamlit run client.py
```

配置（建议）
- 在环境变量中设置你的 API Key，例如：

```powershell
$env:OPENAI_API_KEY = "your_api_key"
# 或在 CI/CD 中使用 Secret 管理
```

- 或创建一个 `config_local.py`（加入 `.gitignore`），示例：

```py
OPENAI_API_KEY = "your_api_key"
OPENAI_BASE_URL = "https://api.your-provider.com/v1"
EMBEDDING_MODEL_NAME = "your-embedding-model"
CHAT_MODEL_NAME = "your-chat-model"
```

运行与调试
- 侧边栏上传 TXT 文件到知识库（会拆分并入库）
- 在主界面输入问题，聊天模型会调用向量检索并返回答案，历史会被保存到 `chat_history.json`


常见问题
- 如果出现批量/速率限制错误，请调整 `configdata.max_embedding_batch_size` 和 `configdata.chunk_size`，并咨询你的模型提供商。
- 若需真实 token 级流式输出，需要后端模型与回调支持，本仓库演示了一个实现方式
