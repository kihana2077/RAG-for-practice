from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import configdata as config

class VectorStoreService(object):
    def __init__(self,embeddings):
        self.embeddings = OpenAIEmbeddings(
            model=config.embedding_model_name,
            api_key=config.openai_api_key,
            base_url=config.openai_base_url,
        )
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embeddings,
            persist_directory=config.persist_directory,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k":config.similarity_threshold})