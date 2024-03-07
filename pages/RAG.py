from st_pages import show_pages_from_config, add_page_title
import streamlit as st
import os
from services import SearchMethod
from dotenv import load_dotenv
from Home import init_qdrantdb

st.set_page_config(page_title="RAG",
                   page_icon=":mag:",
                   layout="wide")

load_dotenv()  # take environment variables from .env.


# ChromaDB connection --> should be cached
if "qdrant_client" in st.session_state:
    qdrant_client = st.session_state["qdrant_client"]
else:
    qdrant_client = init_qdrantdb()
    st.session_state["qdrant_client"] = qdrant_client

if "rag_context" in st.session_state:
    rag_context = st.session_state["rag_context"]
else:
    st.session_state["rag_context"] = None

# collection selections
st.session_state["collection_options"] = qdrant_client.get_collections()

if len(st.session_state["collection_options"]) == 0:
    qdrant_client.create_collection(qdrant_client._collection_name)
    st.session_state["collection_options"] = qdrant_client.get_collections()

if 'selected_collection' not in st.session_state:
    st.session_state["selected_collection"] = st.session_state["collection_options"][0]

def perform_query():
    """
    Retrieve based on user request
    """  
    query = st.session_state["rag_query"]
    selected_retriever = st.session_state["selected_retriever"]
    
    selected_collection = st.session_state["selected_collection"]
    print(f"searching with {selected_retriever} on {selected_collection}")
    hits = qdrant_client(query=query, collection_name=selected_collection, method=SearchMethod(selected_retriever))
    st.session_state["rag_context"] = hits
    print("found these", hits)
    

st.markdown(" # :mag: Retrieval Augmented Generation (RAG)")

st.header("Input")
with st.container(border=True):
    # Selectbox displaying current options with a callback to select an option
    selected_retriever = st.selectbox("Choose a retriever", options=["score", "simsearch", "mmr"], index=st.session_state["collection_options"].index(st.session_state["selected_collection"]))
    
    # Text input for user to enter a new option
    st.text_input("Enter a query", key='rag_query', on_change=None)

    # Button to add the new option to the list
    st.button("Perform query", on_click=perform_query)

    st.session_state["selected_retriever"] = selected_retriever


# RAG results
if st.session_state["rag_context"] is not None:
    st.markdown("**sources**")
    for idx, doc in enumerate(st.session_state["rag_context"]):
        st.markdown(f"**{idx+1}.**")
        st.markdown(f"{doc.page_content}")