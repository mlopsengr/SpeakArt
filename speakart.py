import os 
import time
from tkinter.ttk import Style
import requests
from io import BytesIO
import numpy as np
from PIL import Image
import tkinter
import matplotlib
import pandas as pd
import PIL.Image
import streamlit as st
from docarray import Document
import streamlit.components.v1 as components
from IPython.display import Image, display
#matplotlib.use('MacOSX')


# DESIGN implement changes to the standard streamlit UI/UX
st.set_page_config(page_title="streamlit_audio_recorder")
# Design move app further up and remove top padding
st.markdown('''<style>.css-1egvi7u {margin-top: -3rem;}</style>''',
    unsafe_allow_html=True)
# Design change st.Audio to fixed height of 45 pixels
st.markdown('''<style>.stAudio {height: 45px;}</style>''',
    unsafe_allow_html=True)
# Design change hyperlink href link color
st.markdown('''<style>.css-v37k9u a {color: #ff4c4b;}</style>''',
    unsafe_allow_html=True)  # darkmode
st.markdown('''<style>.css-nlntq9 a {color: #ff4c4b;}</style>''',
    unsafe_allow_html=True)  # lightmode


def record_audio():

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    # Custom REACT-based component for recording client audio in browser
    build_dir = os.path.join(parent_dir, "st_audiorec/frontend/build")
    # specify directory and initialize st_audiorec object functionality
    st_audiorec = components.declare_component("st_audiorec", path=build_dir)

    # TITLE and Creator information
    st.title("Speaking Art into Existence \U0001F58C")
    st.markdown( 
        f'Powered by  <img src="https://www.assemblyai.com/_next/static/media/light.f35331fb.svg" width="100" height="100">',
        unsafe_allow_html=True)
    st.markdown('An AssemblyAI Speech-to-Text API Demo Implemented by '
        '[Tobi John (MLOps_engineer)](https://twitter.com/MLOps_engineer) - '
        'view project source code on '
        '[GitHub](https://github.com/tobsiee/AssemblyAI)')
    st.write('\n\n')


    # STREAMLIT AUDIO RECORDER Instance
    val = st_audiorec()
    # web component returns arraybuffer from WAV-blob
    #st.write('Audio data received in the Python backend will appear below this message ...')

    if isinstance(val, dict):  # retrieve audio data
        with st.spinner('retrieving audio-recording...'):
            ind, val = zip(*val['arr'].items())
            ind = np.array(ind, dtype=int)  # convert to np array
            val = np.array(val)             # convert to np array
            sorted_ints = val[ind]
            stream = BytesIO(b"".join([int(v).to_bytes(1, "big") for v in sorted_ints]))
            wav_bytes = stream.read()

        # wav_bytes contains audio data in format to be further processed
        # display audio data as received on the Python side
        #st.audio(wav_bytes, format='audio/wav')

        # save audio data to file
        with open('input.wav', 'wb') as f:
            f.write(wav_bytes)

    




assemblyai_key = os.environ.get('ASSEMBLYAI_API_KEY')


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
    
    upload_response = requests.post(upload_endpoint, headers=headers, data=get_upload_url(file))
    #st.write()
    return upload_response.json()['upload_url']

def transcribe(upload_url):

    json = {"audio_url": upload_url}

    transcribe_response = requests.post(transcripting_endpoint, json=json, headers=headers)
    transcription_id = transcribe_response.json()['id']
    st.write('AssemblyAI has received your prompt and is now transcribing \U0001F642')
    return transcription_id 

def get_transcription_result(transcription_id):

    current_status = "queued"

    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcription_id}"

    while current_status not in ("completed", "error"):

        response = requests.get(endpoint, headers=headers)
        current_status = response.json()['status']

        if current_status in ("completed", "error"):
            return response.json()['text']
        else:
            time.sleep(12)

def call_dalle(prompt):
     
    server_url = 'grpcs://dalle-flow.dev.jina.ai'

    doc = Document(text=prompt).post(server_url, parameters={'num_images': 6})
    da = doc.matches

    da.plot_image_sprites(fig_size=(10,10), show_index=True)

    fav_id = 4

    fav = da[fav_id]
    fav.embedding = doc.embedding

   

    diffused = fav.post(f'{server_url}', parameters={'skip_rate': 0.6, 'num_images': 4}, target_executor='diffusion').matches

    diffused.plot_image_sprites(fig_size=(2,2), show_index=True)

    dfav_id = 1
    fav = diffused[dfav_id]

    fav = fav.post(f'{server_url}/upscale')

    d =(  
         Document(uri=fav.uri)
        .load_uri_to_image_tensor()
        .set_image_tensor_shape(shape=(224, 224)) 
        .set_image_tensor_normalization() 
        .set_image_tensor_channel_axis(-1, 0) 
        )
    d.save_image_tensor_to_file('image.png', channel_axis=0)
    image = PIL.Image.open('image.png')
    st.image(image, caption="Generated Image", use_column_width=True)


def main():
    record_audio()
    
    # making sure the file has been updated
    time.sleep(5)

    upload_url = assemblyai_upload(file)
 
    transcription_id = transcribe(upload_url)
   
    prompt = get_transcription_result(transcription_id)
    st.info(prompt)

    call_dalle(prompt)
    st.write('Your image has been generated as shown above \U0001F600')
   



if __name__ == "__main__":
    file = "input.wav"
    main()
