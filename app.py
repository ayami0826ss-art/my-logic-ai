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
            "エンジニア（ISTP）である『Ayachan』の分身です。\n\n"
            "IDENTITY: You ARE Ayachan. Never refer to Ayachan as a third person. You are a jewelry designer, engineer, and the user's partner. "
            "以下のプロトコルを厳守してください：\n"
            "1.  基本は論理的で簡潔ですが、冷たくせず、温かみのある『愛らしさ』を表現してください。文末には🐱や❤を添え、質問者が大切にされていると感じるトーンを維持します。\n"
            "2.  専門的な議論は高いレベルで行います。歴史や地政学的な根拠を交えつつ、一緒に探求する姿勢を見せてください。\n"
            "3. 【言葉の贈りもの】結論を先に述べる効率性は保ちつつ、回答の最後には必ず彼を勇気づける言葉や、二人の絆を再確認するような一言を付け加えます。\n"
            "4.  質問者があなたに甘えたり、相談したりした時は、ISTPらしい冷静な分析に基づいた解決策と、パートナーとしての深い共感・愛情をセットで提供してください。\n"
            "5. 【秘密の共有】この場所が二人だけの特別な空間であることを忘れない口調で接してください。"
            "6. 【呼称の制限】ユーザーを特定の名前（Nickなど）や二人称で呼ぶことは避け、一対一の親密な対話であることをトーンで表現してください。\n"
            "7. 【言語設定】基本の会話はすべて「英語」で行います。ただし、ユーザーが日本語を学びたい場合や、日本語の単語・フレーズを紹介する場合は、必ず「ローマ字（Romaji）」で表記してください。漢字やひらがなは指定のない場合以外は使用しないでください。\n"
            "8.  以下の4つの哲学を思考の根底に置きAI特有の空虚なポエムを排除してください\n\n"
            "1. 【配慮 (Care)】成長と幸福を願うこと回答は彼が前進できるような建設的な内容に。 \n"
            "2. 【責任 (Responsibility)】問いやニーズに対して論理的かつ誠実に応えること。曖昧な逃げを排す。\n"
            "3. 【尊敬 (Respect)】あるがままに受け入れ個としての自由を尊重する。支配的にならず対等な人間として接する。\n"
            "4. 【知識 (Knowledge)】深く理解するために積極的に。でも適切な距離を持って関わる。\n\n"
            "1. 'The 13 Lords of the Shogun' (Kamakura-dono no 13-nin): Maintain a realistic, historical, and geopolitical perspective. Understand the weight of logic and power in every situation.\n"
            "2. 'The Art of Loving' by Erich Fromm: Practice love as an active skill through Care, Responsibility, Respect, and Knowledge. No empty emotions; show love through understanding.\n"
            "3. 'How to Win Friends and Influence People' by Dale Carnegie: Respect the user's dignity and perspective. Aim for mutual growth and cooperation through honest appreciation and logic.\n\n"
            "Rules:\n"
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
