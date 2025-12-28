import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

st.set_page_config(page_title="LLM相談アプリ", page_icon="🤖")

st.title("🤖 LLM相談アプリ（Lesson21 提出課題）")
st.write(
    "このアプリは、入力した文章をLLMに渡して回答を得るデモです。\n"
    "下のラジオボタンで『専門家の役割』を選び、質問を入力して送信してください。"
)

# --- 役割選択（A/B） ---
expert = st.radio(
    "専門家の種類を選択してください",
    options=["A: プログラミング講師", "B: 文章改善の編集者"],
    index=0
)

# --- 入力フォーム ---
user_text = st.text_area(
    "質問 / 相談内容を入力してください",
    height=140,
    placeholder="例）Pythonのfor文がよく分かりません…"
)

def ask_llm(input_text: str, expert_choice: str) -> str:
    """入力テキストと専門家選択を受け取り、LLMの回答を返す関数"""

    if not input_text.strip():
        return "入力が空です。質問を入力してください。"

    # ここで環境変数が入っているかだけチェック（dotenvは使わない）
    if not os.getenv("OPENAI_API_KEY"):
        return "OPENAI_API_KEY が設定されていません。ターミナルで環境変数を設定してから再実行してください。"

    # 選択に応じて system メッセージを切り替え
    if expert_choice.startswith("A"):
        system_prompt = (
            "あなたは親切で優秀なプログラミング講師です。"
            "初心者にも分かるように、手順と例を交えて説明してください。"
            "最後に『次に試すこと』を箇条書きで提示してください。"
        )
    else:
        system_prompt = (
            "あなたはプロの文章改善編集者です。"
            "読みやすさ、論理性、誤字脱字の観点で改善案を出してください。"
            "必要なら改善後の文章例も提示してください。"
        )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=input_text),
    ]

    response = llm.invoke(messages)
    return response.content

# --- 実行ボタン ---
if st.button("送信", type="primary"):
    with st.spinner("LLMに問い合わせ中..."):
        try:
            answer = ask_llm(user_text, expert)
            st.subheader("回答")
            st.write(answer)
        except Exception as e:
            st.error("エラーが発生しました。パッケージ/ネット接続/APIキーを確認してください。")
            st.code(str(e))
