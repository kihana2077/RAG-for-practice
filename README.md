# RAG-for-practice

轻量级 RAG（Retrieval-Augmented Generation）练习项目

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://www.python.org/)
[![Langchain](https://img.shields.io/badge/Built_from-langchain-blue)](https://github.com/langchain-ai/langchain)

## 技术栈

| 类别 | 技术 | 说明 |
|------|------|------|
| **LLM 框架** | LangChain | 核心编排框架，管理 Chain、Prompt、Retriever |
| **向量数据库** | Chroma | 轻量级本地向量数据库，支持持久化存储 |
| **嵌入模型** | OpenAI Embeddings | 兼容所有 OpenAI 格式的 Embedding API |
| **对话模型** | OpenAI Chat | 兼容所有 OpenAI 格式的 Chat API |
| **前端** | Streamlit | 快速构建 Web UI，支持文件上传与对话 |
| **文本分割** | LangChain TextSplitter | 支持自定义分块策略 |
| **包管理** | uv / pip | 推荐使用 uv 进行依赖管理 |

## 项目结构

```
RAG-for-practice/
├── client.py              # Streamlit 前端入口
├── rag.py                 # RAG 核心逻辑（Chain 组装、对话、流式输出）
├── knowledge_base.py      # 知识库管理（文档上传、分块、入库）
├── vector_stores.py       # 向量数据库服务封装
├── chat_history.py        # 聊天历史管理（JSON 持久化）
├── configdata.py          # 配置管理（从 .env 读取）
├── file_uploader.py       # 文件上传工具
├── .env.example           # 环境变量模板
├── .env                   # 环境变量（不提交）
└── chroma_db/             # 向量数据库本地存储（不提交）
```

## 功能概览

- **文档处理**：支持 TXT 文件上传，自动分块并存入向量数据库
- **智能问答**：基于向量检索的 RAG 问答，结合上下文生成回答
- **模型兼容**：兼容所有 OpenAI 格式的大模型（LLMs）及嵌入模型（Embedding）
- **聊天历史**：自动保存对话记录，支持上下文连续对话
- **流式输出**：支持 LLM 流式响应，提升交互体验
- **Web 界面**：基于 Streamlit 的可视化操作界面

## 安全与配置

使用 `.env` 文件管理敏感配置（API Key 等）。

1. 复制示例配置文件：

```bash
cp .env.example .env
```

2. 编辑 `.env`，填入你的配置：

```env
CHAT_API_KEY=your_chat_api_key
CHAT_BASE_URL=https://api.your-provider.com/v1
CHAT_MODEL_NAME=your-chat-model

EMBEDDING_API_KEY=your_embedding_api_key
EMBEDDING_BASE_URL=https://api.your-provider.com/v1
EMBEDDING_MODEL_NAME=your-embedding-model
```

## 快速启动

### 方式一：使用 `uv`（推荐）

1. 创建并激活虚拟环境：

```powershell
uv venv
```

2. 安装依赖：

```powershell
uv sync
```

3. 启动前端：

```powershell
streamlit run client.py
```

### 方式二：使用 `pip`

```powershell
pip install -r requirements.txt
streamlit run client.py
```

## 运行与调试

- 侧边栏上传 TXT 文件到知识库（会拆分并入库）
- 在主界面输入问题，聊天模型会调用向量检索并返回答案，历史会被保存到 `chat_history.json`

## 常见问题

- 如果出现批量/速率限制错误，请调整 `configdata.py` 中的 `max_embedding_batch_size` 和 `chunk_size`，并咨询你的模型提供商。
- 若需真实 token 级流式输出，需要后端模型与回调支持，本仓库演示了一个实现方式
