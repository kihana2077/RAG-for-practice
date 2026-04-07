import streamlit as sl
from knowledge_base import KonwledgeBaseService

sl.title("知识库文件上传系统")
new_file = sl.file_uploader(
    label="请上传TXT文件",
    type=['txt'],
    accept_multiple_files=False,
)

if "service" not in sl.session_state:
    sl.session_state["service"] = KonwledgeBaseService()

if new_file is not None:
    file_name = new_file.name
    file_type = new_file.type
    file_size = new_file.size / 1024
    sl.subheader(f"文件名：{file_name}")
    sl.write(f"文件格式：{file_type} | 文件大小：{file_size:.2f}KB")
    text = new_file.getvalue().decode('utf-8')
    result = sl.session_state["service"].upload_by_str(text,file_name)
    sl.write(result)