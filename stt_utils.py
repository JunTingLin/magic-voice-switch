import speech_recognition as sr

def stt_audio(wav_path):
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

def classify_from_text(text):
    class_keywords = {
        1: ["凱蒂", "凱莉", "凱琳"],
        2: ["開燈"],
        3: ["墾丁", "觀點", "冠廷", "觀林", "管麟"],
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

    # 進行STT
    text = stt_audio(wav_path)
    print(f"STT Result: {text}")

    # 進行分類
    label_id, label, raw_text = classify_from_text(text)
    print(f"Detected: {label} with label ID: {label_id}")
    print(f"Raw Text: {raw_text}")
