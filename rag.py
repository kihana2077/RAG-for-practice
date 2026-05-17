from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from vector_stores import VectorStoreService
from chat_history import ChatHistoryService
from services import Services
import configdata as config

def print_prompt(prompt):
    print(prompt.to_string())
    print("="*20)
    return prompt

class DictToStr(Runnable):
    def invoke(self, input, run_manager=None, **kwargs):
        if isinstance(input, dict):
            if "input" in input:
                return str(input["input"])
            return str(input)
        return str(input)

class RagService(object):
    def __init__(self):
        self.vector_service = VectorStoreService()

        self.prompt_template = ChatPromptTemplate(
            [
                ("system","以提供的已知内容为主，结合大模型自身数据库，回答用户问题。参考资料：{context}"),
                ("placeholder", "{chat_history}"),
                ("user","请回答用户提问:{input}"),
            ]
        )

        self.chat_model = Services.get_chat_model()

        self.chat_history_service = ChatHistoryService()

        self.chain = self.__get_chain()
        self.chain_with_history = self.__get_chain_with_history()

    def __get_chain(self):
        retriever = self.vector_service.get_retriever()
        def format_document(docs: list[Document]):  # 把列表迭代为字符串对象
            if not docs:
                return "无相关参考资料"

            return "\n\n".join(
                f"文档片段: {doc.page_content}\n文档元数据: {doc.metadata}"
                for doc in docs
            )

        dict_to_str = DictToStr()
        chain = {
            "input": dict_to_str,
            "context": dict_to_str | retriever | format_document
        } | self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        return chain

    def __get_chain_with_history(self):
        def get_session_history(session_id: str):
            return self.chat_history_service.history

        return RunnableWithMessageHistory(
            runnable=self.chain,
            get_session_history=get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    def ask(self, question, session_id="default"):
        response = self.chain_with_history.invoke(
            {"input": question},
            config={"configurable": {"session_id": session_id}}
        )
        return response

    def ask_stream(self, question, session_id="default"):
        """Native streaming: yields tokens produced by the LLM as they arrive."""
        retriever = self.vector_service.get_retriever()

        # retrieve docs
        try:
            docs = self.vector_service.vector_store.similarity_search(
                question,
                k=config.similarity_threshold,
            )
        except Exception:
            docs = []

        def format_document(docs: list[Document]):
            if not docs:
                return "无相关参考资料"
            return "\n\n".join(
                f"文档片段: {doc.page_content}\n文档元数据: {doc.metadata}"
                for doc in docs
            )

        context = format_document(docs)
        history_text = ""
        try:
            history_text = self.chat_history_service.get_history_text(session_id)
        except Exception:
            history_text = ""

        prompt_text = f"以提供的已知内容为主，回答用户问题。参考资料：{context}\n{history_text}\n请回答用户提问:{question}"

        try:
            stream_llm = Services.get_chat_model(streaming=True)

            for chunk in stream_llm.stream(prompt_text):
                content = getattr(chunk, "content", None)
                if content is None:
                    continue
                yield str(content)
        except Exception as e:
            yield f"[ERROR] {e}"

