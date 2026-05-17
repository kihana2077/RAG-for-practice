from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from pydantic import SecretStr
import configdata as config

#定义工具类用于创建嵌入模型、向量库和聊天模型的单例实例，使所有模块共享同一个实例
class Services:
    _embeddings: OpenAIEmbeddings | None = None
    _vector_store: Chroma | None = None
    _chat_model: ChatOpenAI | None = None

    @classmethod
    def get_embeddings(cls) -> OpenAIEmbeddings:
        if cls._embeddings is None:
            cls._embeddings = OpenAIEmbeddings(
                model=config.embedding_model_name,
                api_key=SecretStr(config.embedding_api_key or config.openai_api_key),
                base_url=(config.embedding_api_base_url or config.openai_base_url),
            )
        return cls._embeddings

    @classmethod
    def get_vector_store(cls) -> Chroma:
        if cls._vector_store is None:
            cls._vector_store = Chroma(
                collection_name=config.collection_name,
                embedding_function=cls.get_embeddings(),
                persist_directory=config.persist_directory,
            )
        return cls._vector_store

    @classmethod
    def get_chat_model(cls, streaming: bool = False) -> ChatOpenAI:
        if streaming:
            return ChatOpenAI(
                model=config.chat_model_name,
                api_key=SecretStr(config.chat_api_key or config.openai_api_key),
                base_url=(config.chat_api_base_url or config.openai_base_url),
                streaming=True,
            )
        if cls._chat_model is None:
            cls._chat_model = ChatOpenAI(
                model=config.chat_model_name,
                api_key=SecretStr(config.chat_api_key or config.openai_api_key),
                base_url=(config.chat_api_base_url or config.openai_base_url),
            )
        return cls._chat_model
