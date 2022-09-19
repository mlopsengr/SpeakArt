# AssemblyAI
AssemblyAI is a deep learning focused company which was originally an NLP
company. One of their most popular products is their speech to text API. 

This project is based of an astonishing post by Ryan O'Connor, a Developer Educator for Machine Learning AI, from AssemblyAI on how DALLE2 works. You can find the original post [here](https://www.assemblyai.com/blog/how-dall-e-2-actually-works/). I highly recommend you to read it before going through this notebook.

From the original post, it can be summarized simply as: "DALL-E 2 can generate semantically plausible photorealistic images given a text prompt, can produce images with specific artistic styles, can produce variations of the same salient features represented in different ways, and can modify existing images"

While DALLE-2 has been used to generate images from text, it can also be used to generate text from audio data, leveraging on AssemblyAI's speech-to-text API. This is what we will be doing in this notebook.

## Dependencies
## What is AssemblyAI?
For my love for music, my audio file says "an artistic impression of several musical instruments"

![image info](./image.png)

## What is Streamlit?
Streamlit is an open-source Python library that makes it easy to create and deploy custom web apps. It is very easy to use and is very powerful. You can find the documentation [here](https://docs.streamlit.io/en/stable/)

## Jina AI
Jina AI is an open-source MLOps framework that allows you to build ncross-modal and multi-modal applications on the cloud. With their [CLIP-as-a-service](https://clip-as-service.jina.ai/) product, they provide free access to DALL·E Flow, an interactive workflow for generating high-definition images from text prompt leveraging on [DALL·E-Mega](https://github.com/borisdayma/dalle-mini), GLID-3 XL, and Stable Diffusion.You can find the documentation [here](https://github.com/jina-ai/dalle-flow/)

## Storing your API key
A standard and safe way to store your API key is by:
echo "export OPENAI_API_KEY='yourkey'" >> ~/.bash_profile
echo "export ASSEMBLY_API_KEY='yourkey'" >> ~/.bash_profile

where 'yourkey' is your API key. And '~/.bash_profile' loads the key into your environment.

to view this Streamlit app on a browser, run it with the following
  command:

    streamlit run speakart.py [ARGUMENTS]