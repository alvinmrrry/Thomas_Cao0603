import requests  # 添加请求库
import streamlit as st

# 使用请求从网络获取数据
try:
    response = requests.get('https://www.example.com')  # 替换为实际的API URL
    response.raise_for_status()  # 检查请求是否成功
    data = response.json()  # 假设返回的是JSON格式的数据
    st.write(data)  # 使用Streamlit打印内容
except requests.exceptions.RequestException as e:
    st.error(f"请求失败: {e}")  # 打印错误信息