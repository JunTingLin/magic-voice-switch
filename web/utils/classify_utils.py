import numpy as np

def load_labels(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            # 使用 split 函數將每行的數字和標籤分開，並僅保留標籤部分
            labels = [line.strip().split(maxsplit=1)[1] for line in f.readlines()]
        return labels
    except Exception as e:
        print(f"Error reading labels file: {e}")
        raise

def set_input_tensor(interpreter, data):
    tensor_index = interpreter.get_input_details()[0]['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:] = data

def classify_audio(interpreter, data, top_k=1):
    """Returns a sorted array of classification results."""
    # set_input_tensor(interpreter, data)
    interpreter.invoke()
    output_details = interpreter.get_output_details()[0]
    output = np.squeeze(interpreter.get_tensor(output_details['index']))

    # If the model is quantized (uint8 data), then dequantize the results
    if output_details['dtype'] == np.uint8:
        scale, zero_point = output_details['quantization']
        output = scale * (output - zero_point)

    ordered = np.argpartition(-output, top_k)
    return [(i, output[i]) for i in ordered[:top_k]]
