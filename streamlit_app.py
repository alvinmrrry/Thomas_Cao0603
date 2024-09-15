import requests  # 添加请求
import json
import streamlit as st

# 使用请求从网络获取数据 2203d27aa32a1d92275134fb632bf009714b2476
url = "https://google.serper.dev/search"



payload = json.dumps({
  "q": st.text_input('Please input the query:')
})
headers = {
  'X-API-KEY': '2203d27aa32a1d92275134fb632bf009714b2476',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

st.write(response.text)