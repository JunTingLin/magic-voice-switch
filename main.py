import argparse
import time
import numpy as np
import tensorflow as tf
import pyaudio
import wave

def load_labels(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            labels = {i: line.strip() for i, line in enumerate(f.readlines())}
        return labels
    except Exception as e:
        print(f"Error reading labels file: {e}")
        raise

def set_input_tensor(interpreter, image):
    tensor_index = interpreter.get_input_details()[0]['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:] = image

def main():
    while (True):
        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument(
            '--model', help='File path of .tflite file.', required=True)
        parser.add_argument(
            '--labels', help='File path of labels file.', required=True)
        args = parser.parse_args()
    
        labels = load_labels(args.labels)
    

        interpreter = tf.lite.Interpreter(args.model)
        # interpreter = Interpreter(args.model)
        
        interpreter.allocate_tensors()
        a = interpreter.get_input_details()[0]['shape']
        print(a)
        getaudio()
        x = np.fromfile(open('output.wav'),np.int32)[11:]

        # x[0, 0] = np.fromfile(open('output.wav'),np.int16)[22:]

        # for i in range(44032):
        #   x[0, i] = np.fromfile(open('output.wav'),np.int16)[22:][i]

        print(x.shape)
        results = classify_audio(interpreter, x)

        label_id, prob = results[0]
        print(labels[label_id],prob)

        if (labels[label_id]=='0 Background Noise') :
            print("Background Noise")
            # time.sleep(0.5)           # 暫停0.5秒，再執行底下接收回應訊息的迴圈

        elif (labels[label_id]=='1 開damn') :
            print("1 開damn")
            # time.sleep(0.5)           # 暫停0.5秒，再執行底下接收回應訊息的迴圈

        elif (labels[label_id]=='2 開燈') :
            print("2 開燈")
            # time.sleep(0.5)           # 暫停0.5秒，再執行底下接收回應訊息的迴圈
        
        time.sleep(0.5)

def classify_audio(interpreter, image, top_k=1):
    """Returns a sorted array of classification results."""
    set_input_tensor(interpreter, image)
    interpreter.invoke()
    output_details = interpreter.get_output_details()[0]
    output = np.squeeze(interpreter.get_tensor(output_details['index']))

    # If the model is quantized (uint8 data), then dequantize the results
    if output_details['dtype'] == np.uint8:
        scale, zero_point = output_details['quantization']
        output = scale * (output - zero_point)

    ordered = np.argpartition(-output, top_k)
    return [(i, output[i]) for i in ordered[:top_k]]

def getaudio():
    p = pyaudio.PyAudio()

    CHANNELS = 1
    FORMAT = pyaudio.paInt16
    CHUNK = 1024
    RATE = 44100
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Start recording!")

    frames = []
    seconds = 2
    for i in range (0, int(RATE/CHUNK*seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Stop recording.")
    stream.stop_stream()
    stream.close()

    p.terminate()

    wf = wave.open("output.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

main()