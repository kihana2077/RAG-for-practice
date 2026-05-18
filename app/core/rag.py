from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from app.services.vector_stores import VectorStoreService
from app.services.chat_history import ChatHistoryService
from app.core.services import Services

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

        self.chat_model = Services.get_chat_model(streaming=True)#三层组件，向量库，提示词，LLM

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
            "context": dict_to_str | retriever | format_document  #尽管retriever可以接收any类型参数，但将纯字典输入将导致语义污染，且浪费算力））
        } | self.prompt_template | print_prompt | self.chat_model | StrOutputParser() #langchain核心CHAIN
        return chain

    def __get_chain_with_history(self):
        def get_session_history(session_id: str):  #未做session id区分，默认一个session，以后补上该逻辑
            return self.chat_history_service.history

        return RunnableWithMessageHistory(
            runnable=self.chain,
            get_session_history=get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )#RunnableWithMessageHistory 把历史管理从 Chain 中解耦出来，Chain 只管检索和生成，历史由外层统一管理。这样 Chain 更纯粹，历史管理更灵活。

    def ask(self, question, session_id="default") -> str: #静态返回
        response = self.chain_with_history.invoke(
            {"input": question},
            config={"configurable": {"session_id": session_id}}
        )
        return response

    def ask_stream(self, question, session_id="default"): #返回一个迭代器，流式输出
        try:
            for chunk in self.chain_with_history.stream(
                {"input": question},
                config={"configurable": {"session_id": session_id}},
            ):
                # StrOutputParser 返回 TextAccessor，直接转 str
                text = str(chunk)
                if text:
                    yield text
        except Exception as e:
            yield f"[ERROR] {e}"

