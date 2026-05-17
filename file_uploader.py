import streamlit as st
from knowledge_base import KnowledgeBaseService

st.title("知识库文件上传系统")
new_file = st.file_uploader(
    label="请上传TXT文件",
    type=['txt'],
    accept_multiple_files=False,
)

if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

if new_file is not None:
    file_name = new_file.name
    file_type = new_file.type
    file_size = new_file.size / 1024
    st.subheader(f"文件名：{file_name}")
    st.write(f"文件格式：{file_type} | 文件大小：{file_size:.2f}KB")
    text = new_file.getvalue().decode('utf-8')
    result = st.session_state["service"].upload_by_str(text,file_name)
    st.write(result)