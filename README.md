# holy-hack-2024-ai-workshop

This Streamlit application uses Retrieval Augmented Generation (RAG) so you can learn about podcasts from the AE Air Data Podcast!
This repository is meant to be a code-along exercise, however the solution is found under the `complete` folder.

We will divide this workshop into 4 parts:

- Setting up the vector database **QDrant** on a Docker instance
- Transcribing audio files using **Whisper**
- 

## 0. Set up configuration
Download the `.env` file.

## 1. Setting up QDrant
This should be the easiest step! Make sure you have you Docker desktop running.
Then open a terminal in the `vectordb` folder.
run the command

`docker-compose up -d`

This will spin up a docker container with a vector database called **QDrant** running on it.


## 2. Transcribing audio files using **Whisper**

### Speech service

Open up the `services/speech2text.py` file.

Complete the `transcribe` function such that it transcribes a file given by the streamlit `st.FileUploader()`.
The function should be called in *pages/Upload_Data.py*.

As a bonus you can write the transcript to a file such that you do not have to perform the transcription again in case you need to redo future steps.

### Splitter

With the transcription, we have unstructured data that can be used to populate a knowledge base.
The first thing we need to do is split the text into chunks.
To do this we have to implement a **splitter** function.
Go to the `services/chunker.py` file and implement the default and semantic splitter.

You can 

This function should also be called in *pages/Upload_Data.py* after the transcript was generated or when a text file was uploaded.

### Upload to QDrant

Lastly we need to add the chunked text to the vector database. The QDrantCustomClient can be used for this. 
Don't worry about calculating embeddings, the client has this covered.


## 3. Implement RAG retrieval strategies

## 4. Implement Chatbot functionality with **Semantic Routing**
