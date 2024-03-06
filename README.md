# holy-hack-2024-ai-workshop

This Streamlit application uses Retrieval Augmented Generation (RAG) so you can learn about podcasts from the AE Air Data Podcast!
This repository is meant to be a code-along exercise, however the solution is found under the `complete` folder.

We will divide this workshop into 4 parts:

- Setting up the vector database **QDrant** on a Docker instance
- Transcribing audio files using **Whisper**
- 



## 1. Setting up QDrant
This should be the easiest step! Make sure you have you Docker desktop running.
Then open a terminal in the `vectordb` folder.
run the command

`docker-compose up -d`

This will spin up a docker container with a vector database called **QDrant** running on it.


## 2. Transcribing audio files using **Whisper**

