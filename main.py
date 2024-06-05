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

def classify_and_print_results(model_path: str, labels_path: str, audio_path: str = 'output.wav') -> tuple:
    """
    Classify audio data using a provided model and print the results.

    Args:
        model_path (str): Path to the TensorFlow Lite model file.
        labels_path (str): Path to the labels file.
        audio_path (str, optional): Path to the audio file. Defaults to 'output.wav'.

    Returns:
        tuple: A tuple containing the detected label and its probability.
    """
    interpreter = tf.lite.Interpreter(model_path)
    interpreter.allocate_tensors()

    labels = load_labels(labels_path)

    audio_data = np.fromfile(open(audio_path), np.int16)[22:]
    results = classify_audio(interpreter, audio_data)

    label_id, prob = results[0]
    return labels[label_id], prob

def stt_function(labels_path: str, stt_mode: str = "google", audio_path: str = 'output.wav') -> tuple:
    """
    Perform speech-to-text (STT) on audio data and classify the text.

    Args:
        labels_path (str): Path to the labels file.
        stt_mode (str, optional): STT mode to use (google or openai). Defaults to "google".
        audio_path (str, optional): Path to the audio file. Defaults to 'output.wav'.

    Returns:
        tuple: A tuple containing the detected label, label ID, and raw text.
    """
    labels = load_labels(labels_path)

    # 使用stt_audio進行語音轉文字
    text = stt_audio(audio_path, mode=stt_mode)

    # 進行分類
    label_id, label, raw_text = classify_from_text(text)

    return labels[label_id], label_id, raw_text

def main():
    mode = input("Please select mode (1: Use Model, 2: Use STT): ").strip()
    if mode not in ['1', '2']:
        print("Invalid selection. Please choose 1 or 2")
        return

    if mode == '2':
        stt_mode = input("Please select STT mode (google/openai): ").strip()
        if stt_mode not in ['google', 'openai']:
            print("Invalid selection. Defaulting to google STT")
            stt_mode = "google"  # Set default value to "google"
    
    if mode == '1':
        print("Model mode selected. Ready to classify audio commands.")
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
            label, prob = classify_and_print_results(model_path=MODEL_PATH, labels_path=LABELS_PATH)
            print(f"Detected: {label} with probability {prob:.4f}")
        else:
            # 使用STT
            label, label_id, raw_text = stt_function(labels_path=LABELS_PATH, stt_mode=stt_mode)
            print(f"Detected: {label} with label ID: {label_id}")
            print(f"Raw Text: {raw_text}")

        time.sleep(0.5)

if __name__ == "__main__":
    main()
