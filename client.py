import streamlit as st
from knowledge_base import KnowledgeBaseService
from rag import RagService
from chat_history import ChatHistoryService
import configdata as config
import time


st.set_page_config(page_title="RAG 聊天助手", layout="wide")

CSS = """
<style>
body { background: #f7f9fb; }
.stApp { max-width: 100%; margin: 0 auto; }
.chat-box { background: #ffffff; padding: 16px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.user { background: #e6f7ff; padding: 10px; border-radius: 8px; margin-bottom:8px }
.ai { background: #f1f3f5; padding: 10px; border-radius: 8px; margin-bottom:8px }
.meta { color: #6b7280; font-size:12px }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def init_services():
    if "kb_service" not in st.session_state:
        st.session_state["kb_service"] = KnowledgeBaseService()
    if "rag" not in st.session_state:
        st.session_state["rag"] = RagService()
    if "history" not in st.session_state:
        st.session_state["history"] = ChatHistoryService()
    if "ai_buffer" not in st.session_state:
        st.session_state["ai_buffer"] = ""


init_services()

kb_service: KnowledgeBaseService = st.session_state["kb_service"]
rag: RagService = st.session_state["rag"]
history: ChatHistoryService = st.session_state["history"]


with st.sidebar:
    st.title("知识库管理")
    uploaded = st.file_uploader("上传 TXT 文档到知识库", type=["txt"], accept_multiple_files=False)
    if uploaded is not None:
        txt = uploaded.getvalue().decode('utf-8')
        filename = uploaded.name
        # 兼容不同方法名
        if hasattr(kb_service, "upload_by_string"):
            res = kb_service.upload_by_str(txt, filename)
        else:
            res = kb_service.upload_by_str(txt, filename)
        st.success(res)

    st.markdown("---")
    st.caption("聊天历史")
    if st.button("清空历史"):
        try:
            history.clear()
        except Exception:
            try:
                history.history.clear()
            except Exception:
                pass
        st.success("已清空")
    st.write("最近消息:")
    msgs = history.get_messages()
    if msgs:
        for m in msgs[-10:]:
            role = getattr(m, 'type', None) or getattr(m, 'role', None) or (m.get('role') if isinstance(m, dict) else 'user')
            content = getattr(m, 'content', None) or (m.get('content') if isinstance(m, dict) else str(m))
            st.markdown(f"**{role}**: {content}")
    else:
        st.write("暂无历史")


st.title("RAG 聊天助手")

col1, col2 = st.columns([3,1])

with col1:
    st.markdown("""
    #### 对话窗口
    在下方输入你的问题，系统会使用你已上传的知识库回答并保留会话历史。
    """)

    user_input = st.text_area("你的问题", height=120)
    if st.button("发送", key="send"):
        if not user_input.strip():
            st.warning("请先输入问题")
        else:
            # 记录用户消息
            try:
                history.add_user_message(user_input)
            except Exception:
                try:
                    history.history.add_user_message(user_input)
                except Exception:
                    pass

            # 使用 langchain 原生流式接口，并把迭代器内容实时写入 session_state['ai_buffer']
            st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
            st.markdown(f"<div class='user'><b>用户:</b> {user_input}</div>", unsafe_allow_html=True)
            out = st.empty()
            out.markdown(f"<div class='ai'><b>AI:</b> </div>", unsafe_allow_html=True)
            st.session_state["ai_buffer"] = ""
            try:
                for token in rag.ask_stream(user_input):
                    st.session_state["ai_buffer"] += token
                    out.markdown(f"<div class='ai'><b>AI:</b> {st.session_state['ai_buffer']}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.session_state["ai_buffer"] += f"\n[ERROR] {e}"
                out.markdown(f"<div class='ai'><b>AI:</b> {st.session_state['ai_buffer']}</div>", unsafe_allow_html=True)

            # 保存完整回答到历史
            try:
                history.add_ai_message(st.session_state["ai_buffer"])
            except Exception:
                try:
                    history.history.add_ai_message(st.session_state["ai_buffer"])
                except Exception:
                    pass

            st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("### 说明")
    st.markdown("- 使用侧边栏上传 TXT 到 Chroma 向量库\n- 聊天历史保存在 `configdata.chat_history_path` 指定的文件\n- 若要重置知识库，请删除 `chroma_db` 目录")
