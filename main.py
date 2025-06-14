import streamlit as st
import openai
import tempfile
import os
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

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

# スピード調整（0.25倍から4倍まで）
speed = st.sidebar.slider(
    "Speed",
    min_value=0.25,
    max_value=4.0,
    value=1.0,
    step=0.25,
    help="音声の再生速度を調整（0.25x - 4.0x）"
)

# --- メイン入力 ---
text_input = st.text_area(
    "Enter text to convert to speech:",
    value="The quick brown fox jumped over the lazy dog."
)

if st.button("Generate Speech"):
    # APIキー未入力チェック
    if not api_key:
        st.error("OpenAI APIキーが設定されていません。サイドバーに入力してください。")
    elif not text_input.strip():
        st.error("変換するテキストを入力してください。")
    else:
        with st.spinner("Generating audio..."):
            try:
                # 一時ファイル作成
                tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                # 音声生成リクエスト（スピードパラメータを追加）
                with openai.audio.speech.with_streaming_response.create(
                    model=model,
                    voice=voice,
                    input=text_input,
                    speed=speed  # スピード調整パラメータを追加
                ) as response:
                    response.stream_to_file(tmpfile.name)

                # ファイルを読み込み再生
                audio_bytes = open(tmpfile.name, "rb").read()
                st.success("Audio generation complete!")
                st.audio(audio_bytes, format="audio/mp3")
                
                # スピード情報を表示
                st.info(f"Generated with speed: {speed}x")
            except Exception as e:
                st.error(f"An error occurred: {e}")