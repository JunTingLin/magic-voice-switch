import os
from openai import AzureOpenAI
from dotenv import find_dotenv, load_dotenv

_ = load_dotenv(find_dotenv())

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"], 
    api_key=os.environ["AZURE_OPENAI_API_KEY"],  
    api_version="2023-05-15"
)

deployment_id = os.environ["AZURE_DEPLOYMENT_NAME"]

audio_test_file = "./output.wav"

result = client.audio.transcriptions.create(
    file=open(audio_test_file, "rb"),            
    model=deployment_id
)

print(result)
