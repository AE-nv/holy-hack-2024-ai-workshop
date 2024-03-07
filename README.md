# holy-hack-2024-ai-workshop

This Streamlit application uses Retrieval Augmented Generation (RAG) so you can learn about podcasts from the AE Air Data Podcast!
This repository is meant to be a code-along exercise, however the solution is found under the `complete` folder.

We will divide this workshop into 4 parts:

- Setting up the vector database **QDrant** on a Docker instance
- Transcribing audio files using **Whisper**
- 

## 0. Set up configuration
Download the `.env` file. Make sure it is called .env.

### With Poetry 
...

In order to make sure the environment is made in your root folder, run the following line

`poetry config virtualenvs.in-project true`

Run `Poetry install` in the root folder. This will install the dependencies defined in pyproject.toml

### With Virtualenv
...


## 1. Setting up QDrant
This should be the easiest step! Make sure you have you Docker desktop running.
Then open a terminal in the `vectordb` folder.
run the command

`docker-compose up -d`

The -d flag simply means that we are detached from the container such that the terminal is not occupied.

This will spin up a docker container with a vector database called **QDrant** running on it.

Go back to your root folder. Now you can run the streamlit app for the first time with

`streamlit run Home.py`

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

In the *pages/Upload_Data.py* finish the set of function calls. You can use the **QDRantCustomClient** which is available as `qdrant_client`. Checkout the `services/vectordb.py` to find out which function to call.

## 3. Implement RAG retrieval strategies

We will implement three simple retrievers:
- `score`
- `simsearch`
- `mmr` : Maximal Marginal Relevance

These can be found in the **QdrantCustomClient** in the `services/vectordb.py` file.
You can use the **QDrant** object of the class to perform the retrievals.

After this you can test the retrievers on the RAG page.

## 4. Implement Chatbot functionality with **Semantic Routing**


