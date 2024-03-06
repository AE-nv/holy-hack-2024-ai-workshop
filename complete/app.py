import streamlit as st
from st_pages import show_pages_from_config, add_page_title
from services import QDrantCustomClient, SemanticRouter
from langchain_openai import AzureOpenAIEmbeddings
from dotenv import load_dotenv

# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
add_page_title()

show_pages_from_config()

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
Welcome to the Air Data Chatbot!

This chatbot knows all about the podcast Air Data (add link) and can answer any questions you may have.

"""


st.text(welcome_message)

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

