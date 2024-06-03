import os

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

_ = load_dotenv(find_dotenv())

# Set the environment variable
api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()

audio_file= open("./output.wav", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)

print(transcription.text)
