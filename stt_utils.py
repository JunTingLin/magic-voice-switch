import os
import speech_recognition as sr
import openai
from dotenv import load_dotenv

# 加載 .env 文件中的環境變量
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 使用 Google Speech Recognition
def stt_google(wav_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data, language='zh-TW')
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"

# 使用 OpenAI Whisper STT
def stt_openai(wav_path):
    prompt = "Transcribe the following audio into text:"
    with open(wav_path, "rb") as audio_file:
        response = openai.Audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            prompt=prompt
        )
        return response["text"]

# 統一的 STT 接口
def stt_audio(wav_path, mode="google"):
    if mode == "google":
        return stt_google(wav_path)
    elif mode == "openai":
        return stt_openai(wav_path)
    else:
        raise ValueError(f"Unknown mode: {mode}")

def classify_from_text(text):
    class_keywords = {
        1: ["凱蒂", "凱莉", "凱琳"],
        2: ["開燈"],
        3: ["墾丁", "觀點", "冠廷", "觀林", "管麟", "one day", "腕力", "婉婷", "碗蓮", "管理", "觀音"],
        4: ["關燈"]
    }

    if text == "":
        return 0, "Background Noise", text

    for class_id, keywords in class_keywords.items():
        if any(keyword in text for keyword in keywords):
            return class_id, {1: "開damn", 2: "開燈", 3: "關damn", 4: "關燈"}[class_id], text

    return 0, "Background Noise", text

if __name__ == "__main__":
    # 測試錄音文件
    wav_path = "output.wav"

    # 選擇 STT 模式（google 或 openai）
    mode = input("請選擇STT模式 (google/openai): ").strip()

    # 進行STT
    text = stt_audio(wav_path, mode)
    print(f"STT Result: {text}")

    # 進行分類
    label_id, label, raw_text = classify_from_text(text)
    print(f"Detected: {label} with label ID: {label_id}")
    print(f"Raw Text: {raw_text}")
