import pyaudio
import wave

def get_audio(output_path="output.wav", duration=1, channels=1, rate=44100, chunk=1024):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    # print("Start recording!")

    frames = []
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Stop recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(output_path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    print(f"Audio recorded and saved to {output_path}")

def read_audio(file_path):
    with wave.open(file_path, 'rb') as wf:
        frames = wf.readframes(wf.getnframes())
    return frames
