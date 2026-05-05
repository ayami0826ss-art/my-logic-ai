import streamlit as st
from groq import Groq

# ページの設定
st.set_page_config(page_title="Logic Culture AI", page_icon="⛩️")
st.title("論理的・日本文化学習AI")

# APIキーの設定（Secretsから読み込む設定）
# まだSecretsを設定していない場合は、一時的にここに直接書いても動きます
# client = Groq(api_key="gsk_...") 
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# セッション状態（履歴）の保持
if "messages" not in st.session_state:
    st.session_state.messages = []

# 過去のメッセージを表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザー入力
if prompt := st.chat_input("日本文化や言語のロジックを質問してください"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AIの回答生成
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        messages = [
            {"role": "system", "content": "あなたは論理的・構造的な視点を持つ専門家です。簡潔で分析的な回答をしてください。"}
        ] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            stream=True
        )

        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                full_response += content
                response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
