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

}