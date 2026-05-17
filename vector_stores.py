from services import Services
import configdata as config


class VectorStoreService(object):
    def __init__(self):
        self.vector_store = Services.get_vector_store()

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k":config.similarity_threshold})