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
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py          # 导出 RagService, Services
│   │   ├── rag.py               # RAG 核心逻辑（Chain 组装、对话、流式输出）
│   │   └── services.py          # 共享组件单例（Embeddings、Chroma、ChatOpenAI）
│   ├── services/
│   │   ├── __init__.py          # 导出 KnowledgeBaseService, VectorStoreService, ChatHistoryService
│   │   ├── knowledge_base.py    # 知识库管理（文档上传、分块、入库）
│   │   ├── vector_stores.py     # 向量数据库服务封装
│   │   └── chat_history.py      # 聊天历史管理（JSON 持久化）
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py          # 配置管理（从 .env 读取）
│   └── ui/
│       ├── __init__.py
│       ├── client.py            # Streamlit 前端入口
│       └── file_uploader.py     # 文件上传工具
├── chat.py                      # 终端聊天入口
├── .env.example                 # 环境变量模板
├── .env                         # 环境变量（不提交）
└── chroma_db/                   # 向量数据库本地存储（不提交）
```

## 功能概览

- **文档处理**：支持 TXT 文件上传，自动分块并存入向量数据库
- **智能问答**：基于向量检索的 RAG 问答，结合上下文生成回答
- **模型兼容**：兼容所有 OpenAI 格式的大模型（LLMs）及嵌入模型（Embedding）
- **聊天历史**：自动保存对话记录，支持上下文连续对话
- **流式输出**：支持 LLM 流式响应，逐 token 输出
- **双入口**：Web 界面（Streamlit）+ 终端聊天（chat.py）
- **共享组件**：单例模式管理 Embeddings、Chroma、ChatOpenAI，避免重复创建

## 安全与配置

使用 `.env` 文件管理敏感配置（API Key 等）。

1. 复制示例配置文件：

```bash
cp .env.example .env
```

2. 编辑 `.env`，填入你的配置：

```env
# API Key 配置
OPENAI_API_KEY=
EMBEDDING_API_KEY=
CHAT_API_KEY=

# Base URL 配置
OPENAI_BASE_URL=
EMBEDDING_BASE_URL=
CHAT_BASE_URL=

# 模型名称配置
EMBEDDING_MODEL_NAME=
CHAT_MODEL_NAME=
```

## 快速启动

### 方式一：使用 `uv`（推荐）

```powershell
uv venv
uv sync
```

### 方式二：使用 `pip`

```powershell
pip install -r requirements.txt
```

### 启动

```powershell
# Web 界面
streamlit run app/ui/client.py

# 终端聊天
python chat.py
```

## 运行与调试

- **Web 界面**：侧边栏上传 TXT 文件到知识库，主界面输入问题进行对话
- **终端聊天**：直接运行 `python chat.py`，支持流式输出
- **聊天历史**：自动保存到 `chat_history.json`

## 架构设计

- **LangChain Chain**：声明式管道 `retriever → prompt → LLM → output`
- **单例服务**：`Services` 类统一管理 Embeddings、Chroma、ChatOpenAI 实例
- **流式输出**：Chain 原生支持 `stream()`，`ask_stream` 与 `ask` 共享同一套逻辑
- **历史管理**：`RunnableWithMessageHistory` 自动注入/保存对话历史

## 常见问题

- 如果出现批量/速率限制错误，请调整 `app/config/settings.py` 中的 `max_embedding_batch_size` 和 `chunk_size`
- 若出现 `APIConnectionError`，检查 `.env` 中的 API Key 和 Base URL 是否正确
- 若出现 `401 Unauthorized`，API Key 可能已过期，需要重新获取
