import os
import time
import threading
import numpy as np
import tensorflow as tf
from audio_utils import get_audio, read_audio
from classify_utils import load_labels, classify_audio
from stt_utils import stt_audio, classify_from_text

# 設定模型和標籤文件的路徑
MODEL_DIR = 'models'
MODEL_FILE = 'soundclassifier_with_metadata.tflite'
LABELS_FILE = 'labels.txt'
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILE)
LABELS_PATH = os.path.join(MODEL_DIR, LABELS_FILE)

def classify_and_print_results(interpreter, labels, audio_path='output.wav'):
    audio_data = np.fromfile(open(audio_path), np.int16)[22:]
    results = classify_audio(interpreter, audio_data)

    label_id, prob = results[0]
    print(f"Detected: {labels[label_id]} with probability {prob:.4f}")

def stt_function(labels, stt_mode, audio_path='output.wav'):
    # 使用stt_audio進行語音轉文字
    text = stt_audio(audio_path, mode=stt_mode)
    print(f"STT Result: {text}")

    # 進行分類
    label_id, label, raw_text = classify_from_text(text)
    print(f"Detected: {labels[label_id]} with label ID: {label_id}")
    print(f"Raw Text: {raw_text}")



def main():
    mode = input("請選擇模式 (1: 使用模型, 2: 使用STT): ").strip()
    if mode not in ['1', '2']:
        print("無效的選擇，請選擇1或2")
        return

    if mode == '2':
        stt_mode = input("請選擇STT模式 (google/openai): ").strip()
        if stt_mode not in ['google', 'openai']:
            print("無效的選擇，請選擇google或openai")
            return
    
    labels = load_labels(LABELS_PATH)
    
    if mode == '1':
        interpreter = tf.lite.Interpreter(MODEL_PATH)
        interpreter.allocate_tensors()
        print("Interpreter initialized. Ready to classify audio commands.")
        duration = 1  # 模型模式下的錄音時間為1秒
    else:
        print(f"STT mode ({stt_mode}) selected. Ready to transcribe audio.")
        duration = 3  # STT模式下的錄音時間為3秒

    while True:
        # 使用多線程進行音頻錄製
        audio_thread = threading.Thread(target=get_audio, args=("output.wav", duration))
        audio_thread.start()
        audio_thread.join()

        if mode == '1':
            # 開始推理
            classify_thread = threading.Thread(target=classify_and_print_results, args=(interpreter, labels))
            classify_thread.start()
            classify_thread.join()
        else:
            # 使用STT
            stt_thread = threading.Thread(target=stt_function, args=(labels, stt_mode))
            stt_thread.start()
            stt_thread.join()

        time.sleep(0.5)

if __name__ == "__main__":
    main()
