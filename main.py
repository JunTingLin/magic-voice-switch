import os
import time
import numpy as np
import tensorflow as tf
from audio_utils import get_audio, read_audio
from classify_utils import load_labels, classify_audio

# 設定模型和標籤文件的路徑
MODEL_DIR = 'models'
MODEL_FILE = 'soundclassifier_with_metadata.tflite'
LABELS_FILE = 'labels.txt'
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILE)
LABELS_PATH = os.path.join(MODEL_DIR, LABELS_FILE)


def main():
    labels = load_labels(LABELS_PATH)
    interpreter = tf.lite.Interpreter(MODEL_PATH)
    interpreter.allocate_tensors()

    print("Interpreter initialized. Ready to classify audio commands.")

    while True:
        get_audio()
        audio_data = np.fromfile(open('output.wav'), np.int16)[22:]

        print("Audio data shape:", audio_data.shape)
        results = classify_audio(interpreter, audio_data)

        label_id, prob = results[0]
        print(f"Detected: {labels[label_id]} with probability {prob:.4f}")

        if labels[label_id] == '0 Background Noise':
            print("0 Background Noise")
        elif labels[label_id] == '1 開damn':
            print("1 開damn")
        elif labels[label_id] == '2 開燈':
            print("2 開燈")
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()
