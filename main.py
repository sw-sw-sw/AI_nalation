import streamlit as st
import openai
import tempfile
from key import OPENAI_API_KEY

# Streamlitアプリタイトル
st.title("Text-to-Speech with GPT-4o Mini TTS")

# --- APIキー入力 ---
st.sidebar.header("OpenAI Settings")
api_key = st.sidebar.text_input(
    "OpenAI API Key",
    value=OPENAI_API_KEY,  # デフォルト値としてkey.pyから取得
    type="password",
    help="ここにOpenAIのAPIキーを入力してください。"
)
if not api_key:
    st.sidebar.warning("APIキーが設定されていません。入力してください。")
openai.api_key = api_key

# --- TTSモデル設定 ---
st.sidebar.header("TTS Settings")
model = st.sidebar.selectbox(
    "Model",
    ["tts-1", "tts-1-hd"],
    help="使用するTTSモデルを指定"
)

# 日本語コンテンツの場合、FableとNovaが現在最も良い結果を出すとされています
voice_options = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

voice = st.sidebar.selectbox(
    "Voice",
    voice_options,
    help="使用する音声を選択"
)

# --- メイン入力 ---
text_input = st.text_area(
    "Enter text to convert to speech:",
    value="The quick brown fox jumped over the lazy dog."
)

if st.button("Generate Speech"):
    # APIキー未入力チェック
    if not openai.api_key:
        st.error("OpenAI APIキーが設定されていません。サイドバーに入力してください。")
    elif not text_input.strip():
        st.error("変換するテキストを入力してください。")
    else:
        with st.spinner("Generating audio..."):
            try:
                # 一時ファイル作成
                tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                # 音声生成リクエスト
                with openai.audio.speech.with_streaming_response.create(
                    model=model,
                    voice=voice,
                    input=text_input
                ) as response:
                    response.stream_to_file(tmpfile.name)

                # ファイルを読み込み再生
                audio_bytes = open(tmpfile.name, "rb").read()
                st.success("Audio generation complete!")
                st.audio(audio_bytes, format="audio/mp3")
            except Exception as e:
                st.error(f"An error occurred: {e}")
