
from openai import AzureOpenAI
import os

def transcribe(file):
    """
    """

    # Azure openAI Whisper call
    client = AzureOpenAI(azure_endpoint=os.getenv("AZ_OPENAI_WHISPER_ENDPOINT"),
                         azure_deployment=os.getenv("AZ_OPENAI_WHISPER_MODEL"),
                         api_key=os.getenv("AZ_OPENAI_WHISPER_KEY"),
                         api_version=os.getenv("AZ_OPENAI_WHISPER_API_VERSION"))
    

    try: 
        transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=file, 
        response_format="verbose_json",
        language='nl'
        )


        return transcript.text
    except Exception as e:
        print(e)
        raise e
