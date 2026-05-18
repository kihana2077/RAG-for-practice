import os
from dotenv import load_dotenv

load_dotenv()

md5_path = "./md5_file.txt"

#Chroma
collection_name = "RAG"
persist_directory= "./chroma_db"

#splitter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n","\n","。","！",".","!"]
max_split_char_number = 1000
max_embedding_batch_size = 64

# API Key 配置（从环境变量读取）
openai_api_key = os.environ.get("OPENAI_API_KEY", "")
embedding_api_key = os.environ.get("EMBEDDING_API_KEY", "")
chat_api_key = os.environ.get("CHAT_API_KEY", "")

# Base URL 配置（从环境变量读取）
openai_base_url = os.environ.get("OPENAI_BASE_URL", "")
embedding_api_base_url = os.environ.get("EMBEDDING_BASE_URL", "")
chat_api_base_url = os.environ.get("CHAT_BASE_URL", "")

# 模型名称配置（从环境变量读取）
embedding_model_name = os.environ.get("EMBEDDING_MODEL_NAME", "")
chat_model_name = os.environ.get("CHAT_MODEL_NAME", "")

similarity_threshold = 2 #相似度匹配文本数量

# Chat History
chat_history_path = "./chat_history.json"