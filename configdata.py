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

# OpenAI Embeddings
openai_api_key = ""  # 替换为你的API密钥
openai_base_url = ""  # 替换为自定义提供商的base URL
embedding_model_name = ""  # 或其他兼容的嵌入模型名称
chat_model_name = ""

similarity_threshold = 2 #相似度匹配文本数量

# Chat History
chat_history_path = "./chat_history.json"