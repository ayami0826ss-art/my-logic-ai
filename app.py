import streamlit as st
from groq import Groq

# 1. ページの設定
st.set_page_config(page_title="Logic Culture AI", page_icon="⛩️")
st.title("論理的・日本文化学習AI")

# 2. APIキーの設定
# StreamlitのSecretsから読み込みます
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. セッション状態（履歴）の保持
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. 過去のメッセージを表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. ユーザー入力があった時の処理
if prompt := st.chat_input("日本文化や言語のロジックを質問してください"):
    # ユーザーの入力を履歴に追加して表示
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 6. AIの回答生成
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # メッセージリストを構築
        messages = [{"role": "system", "content": "あなたは論理的な専門家です。"}]
        for m in st.session_state.messages:
            messages.append({"role": m["role"], "content": m["content"]})

# API呼び出し（ストリーミング形式）
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # ここを最新の名前に変更
                messages=messages,
                stream=True
            )

            for chunk in completion:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            
            # 回答を履歴に追加
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
