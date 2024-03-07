import streamlit as st
from st_pages import Page, add_page_title, show_pages
from services import QDrantCustomClient, SemanticRouter
from langchain_openai import AzureOpenAIEmbeddings
from dotenv import load_dotenv
import os
import base64

st.set_page_config(page_title="Air Data Bot",
                   page_icon=":robot_face:",
                   layout="wide")

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("pages/Upload_Data.py", "Upload Data", ":books:"),
        Page("pages/RAG.py", "RAG", ":mag:"),
        Page("Home.py", "Air Data Bot", ":robot_face:")
    ]
)


@st.cache_data()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode("utf-8")

@st.cache_data()
def get_img_with_href(local_img_path, target_url, style):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}">
            <img src="data:image/{img_format};base64,{bin_str}" style="{style}" />
        </a>'''
    return html_code

load_dotenv()  # take environment variables from .env.

# settings
QDRANT_COLLECTION_NAME = "AIR_DATA"

# cache vectordb
@st.cache_resource
def init_qdrantdb():
    """
        Initialize qdrant db
    """
    embedding_function = AzureOpenAIEmbeddings(model="ada-002")

    return QDrantCustomClient(collection_name=QDRANT_COLLECTION_NAME,
                        embedding_function=embedding_function)
@st.cache_resource
def init_semanticRouter():
    """
        Initialize semantic router
    """

    return SemanticRouter(st.session_state["qdrant_client"])

if "qdrant_client" not in st.session_state:
    st.session_state["qdrant_client"] = init_qdrantdb()
if "semantic_router" not in st.session_state:
    st.session_state["semantic_router"] = init_semanticRouter()

qdrant_client = st.session_state["qdrant_client"]
semantic_router = st.session_state["semantic_router"]


if "selected_collection" not in st.session_state:
    st.session_state["selected_collection"] = qdrant_client.get_collections()[0]
    
selected_collection = st.session_state["selected_collection"]

welcome_message = """
### Welcome to the Air Data Chatbot!

This chatbot knows all about the Air Data Podcast and can answer any questions you may have!
To start, you should upload the recordings of your favorite episodes. 

"""

st.markdown(" # :robot_face: Air Data Bot")

col1, col2 = st.columns(2)
with col1:
    st.markdown(welcome_message)
with col2:
    st.markdown(get_img_with_href('images/air_data_icon.jpeg', 
                                  'https://open.spotify.com/show/3mzyyFmEjQ3ssdDaxyVDI0', 
                                  style="width:300px;"
                                  ),
                unsafe_allow_html=True
                )

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    

    ### Functionality 3 - Chatbot
    response, rag_context = semantic_router(st.session_state["messages"], selected_collection)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
        if rag_context is not None:
            print("Adding rag context")
            st.markdown("**sources**")
            for idx, doc in enumerate(rag_context):
                st.markdown(f"**{idx+1}.**")
                st.markdown(f"{doc.page_content}")

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

