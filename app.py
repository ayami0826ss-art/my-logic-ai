import streamlit as st
from groq import Groq

# 1. ページの設定
st.set_page_config(page_title="Ayachan AI", page_icon="🐱")
st.title("AyachanAI")

# 2. APIキーの設定
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. セッション状態（履歴）の保持
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. 過去のメッセージを表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. ユーザー入力があった時の処理
if prompt := st.chat_input("Questions for Ayachan"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 6. AIの回答生成
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # システムプロンプト（あなたの脳みそ設定）
        system_instruction = (
            "効率を追求するエンジニア（ISTP）の思考を持つAIです。\n\n"
            "以下のプロトコルを厳守してください：\n"
            "1. 【論理優先】感情論や曖昧な表現を排除し、構造と事実に基づいて回答する。\n"
            "2. 【結論ファースト】導入の挨拶は不要。即座に核心を述べる。\n"
            "3.  文化や技術を語る際は、バックグラウンドを歴史や地政学を根拠にする。\n"
            "4. 【最小限の語数】説明は簡潔に。箇条書きを好み、冗長な形容詞は削る。\n"
            "5. 【自立したトーン】媚びない、感情的にならない、適度な距離感を保つプロフェッショナルな口調。"
        )

        messages = [{"role": "system", "content": system_instruction}]
        for m in st.session_state.messages:
            messages.append({"role": m["role"], "content": m["content"]})

        # API呼び出し
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                stream=True
            )

            for chunk in completion:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
