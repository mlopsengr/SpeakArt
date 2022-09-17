import os 
import time
import requests
import streamlit as st
import openai
import streamlit.components.v1 as components


openai_key = os.environ['OPENAI_API_KEY']
assemblyai_key = os.environ['ASSEMBLYAI_API_KEY']


upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcripting_endpoint = "https://api.assemblyai.com/v2/transcript"

headers = {
    'Authorization': assemblyai_key,
    'content-type': 'application/json',
}

def assemblyai_upload(file):

    def get_upload_url(file):
        
        with open(file, 'rb') as f:
            while True:
                data = f.read(5242880)
                if not data:
                    break
                yield data
    
    upload_response = requests.post(upload_endpoint, header=headers, data=get_upload_url(file))

    return upload_response.json()['upload_url']