# holy-hack-2024-ai-workshop
![alt text](images/air_data_icon.jpeg)

This Streamlit application uses Retrieval Augmented Generation (RAG) so you can learn about podcasts from the AE Air Data Podcast!
This repository is meant to be a code-along exercise, however the solution is found under the `complete` folder.

As an orchestration framework we use **LangChain**, however you can also checkout **LlamaIndex**.

We will divide this workshop into 4 parts:

- Setting up the vector database **QDrant** on a Docker instance
- Transcribing audio files using **Whisper**
- 

## 0. Set up configuration
Download the `.env` file. Make sure it is called .env.

### With Poetry 

In order to make sure the environment is made in your root folder, run the following line

- `poetry config virtualenvs.in-project true`

Run `poetry install` in the root folder. This will install the dependencies defined in pyproject.toml

Then you can use your environment by calling `poetry shell`.

### With Virtualenv
If you have Virtualenv or Anaconda, you can use the *requirements.txt* file to install the dependencies.

The simplest way with **virtualenv** for me would be:

1. create local environment with the right Python executable (>= 3.9)!
- `python -m virtualenv .venv`

2. Activate the environment
- (Windows)

    - `.venv/Scripts/Activate.ps1` (Powershell)

    - `.venv/Scripts/Activate.bat` (CMD)

- (POSIX)

    - `source /.venv/bin/activate`


3. Install dependencies

- `pip install -r requirements.txt`

(With **venv** only the first step would be different `python -m venv .venv`)


## 1. Setting up QDrant
This should be the easiest step! Make sure you have you **Docker desktop** running.
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
The function is called in *pages/Upload_Data.py*.

Note that we also write the transcript to a folder under *data/app/transcripts*. 
If something after the transcribe function fails or you cannot get it to work, you can always upload the transcript txt file instead, so you can continue with the next part.

### Splitter

With the transcription, we have unstructured data that can be used to populate a knowledge base.
The first thing we need to do is split the text into chunks.
To do this we have to implement a **splitter** function.
Go to the `services/chunker.py` file and implement the default and semantic splitter.

You can 

This function is called in *pages/Upload_Data.py* after the transcript was generated or when a text file was uploaded.

### Upload to QDrant

Lastly we need to add the chunked text to the vector database. The QDrantCustomClient can be used for this. 
Don't worry about calculating embeddings, the client has this covered.

In the *pages/Upload_Data.py* this function is called for you, so you're lucky!

## 3. Implement RAG retrieval strategies
Definitely check out https://python.langchain.com/docs/modules/data_connection/retrievers/ for interesting strategies!

We are only covering scoring mechanisms to retrieve documents from our vector database.
We will implement three simple scoring mechanisms:
- `score`
- `simsearch`
- `mmr` (Maximal Marginal Relevance)

These can be found in the **QdrantCustomClient** in the `services/vectordb.py` file.
You can use the **QDrant** object of the class to perform the retrievals.

After this you can test the retrievers on the RAG page. Play with the parameters and compare the retrieved documents.

## 4. Implement Chatbot functionality with **Semantic Routing**

The final step of our application is to implement a chatbot.
We will use a new technique called **Semantic Routing** in order to avoid calling our QDrant client in unneccessary cases.
You can find more information on this technique here: https://github.com/aurelio-labs/semantic-router

Open up the `services/chat.py` file.

You have to complete the following:
- Define routes using the `Route` class
- Define a routing layer using the `RouteLayer` class
- Prompt engineer a system prompt template for your RAG completion call
- Reroute the user query with the `semantic_layer` function
- Implement the different route functions (by default you have `_nonsense`, `_chitchat_completion` and `_rag_completion`)

Once this is done, you should be able to use the chatbot found in the App!

you just implemented a chatbot that uses **RAG** and **Semantic Routing**!


## 5. Extensions

- We only used the last user message as a query for RAG. You can do much more with the chat history. For example one can summarize it with a LLM Completion call and use that summary as an input query for retrieval.
- We did not explore complex Retrieval Strategies such as **FLARE** (https://github.com/jzbjyb/FLARE). If you want to get even better responses, this is something to look into. 
- We simply saved the chunks of text from our transcript. A vector database like QDrant also allows us to store metadata with vectors. You could for example add the timings of the transcript as tags or try speaker identification to chunk the text based on speakers, adding this as a tag as well. You could then also improve your search results by defining a Filter on these tags and performing **Hybrid Search**





