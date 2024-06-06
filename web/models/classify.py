import json
import os

import numpy as np
import tensorflow as tf
from utils.classify_utils import classify_audio, load_labels


def classify_and_print_results(
        model_path: str, labels_path: str, 
        audio_path: str = os.path.join('templates', 'output.wav')) -> str:
    """
    Classify audio data using a provided model and print the results.

    Args:
        model_path (str): Path to the TensorFlow Lite model file.
        labels_path (str): Path to the labels file.
        audio_path (str, optional): Path to the audio file. Defaults to 'output.wav'.

    Returns:
        str: JSON string containing the detected label and its probability.
    """
    interpreter = tf.lite.Interpreter(model_path)
    interpreter.allocate_tensors()

    labels = load_labels(labels_path)

    audio_data = np.fromfile(open(audio_path), np.int16)[22:]
    results = classify_audio(interpreter, audio_data)

    label_id, prob = results[0]
    # Convert label_id and prob to standard Python types
    label_id = int(label_id)
    prob = float(prob)
    result_dict = {
        "label_id": label_id,
        "label": labels[label_id],
        "probability": prob
    }
    print(result_dict)
    return json.dumps(result_dict, ensure_ascii=False)
