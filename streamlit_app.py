import requests  # 添加请求库

# 使用请求从网络获取数据
response = requests.get('https://api.example.com/data')  # 替换为实际的API URL
data = response.json()  # 假设返回的是JSON格式的数据

# 打印获取的数据
st.write(data)  # 使用Streamlit打印内容