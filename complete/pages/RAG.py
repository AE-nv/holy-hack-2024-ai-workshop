from st_pages import Page, add_page_title, show_pages
import streamlit as st
import os
from services import SearchMethod
from dotenv import load_dotenv
from Home import init_qdrantdb

st.set_page_config(page_title="RAG",
                   page_icon=":mag:",
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

load_dotenv()  # take environment variables from .env.


### SETTINGS
# ChromaDB connection
if "qdrant_client" in st.session_state:
    qdrant_client = st.session_state["qdrant_client"]
else:
    qdrant_client = init_qdrantdb()
    st.session_state["qdrant_client"] = qdrant_client

# rag context
if "rag_context" in st.session_state:
    rag_context = st.session_state["rag_context"]
else:
    st.session_state["rag_context"] = None

# RAG retriever settings
if "rag_k" not in st.session_state:
    st.session_state["rag_k"] = 1

if "rag_fetch_k" not in st.session_state:
    st.session_state["rag_fetch_k"] = 2

if "rag_options" not in st.session_state:
    st.session_state["rag_options"] = ["score", "simsearch", "mmr"]

if "selected_rag" not in st.session_state:
    st.session_state["selected_rag"] = st.session_state["rag_options"][0]

# collection selections
st.session_state["collection_options"] = qdrant_client.get_collections()

if len(st.session_state["collection_options"]) == 0:
    qdrant_client.create_collection(qdrant_client._collection_name)
    st.session_state["collection_options"] = qdrant_client.get_collections()

if 'selected_collection' not in st.session_state:
    st.session_state["selected_collection"] = st.session_state["collection_options"][0]

### FUNCTIONS
def perform_query():
    """
    Retrieve based on user request
    """  
    query = st.session_state["rag_query"]
    selected_retriever = st.session_state["selected_retriever"]
    
    selected_collection = st.session_state["selected_collection"]
    print(f"searching with {selected_retriever} on {selected_collection}")
    args = {}
    args["k"] = st.session_state["rag_k"]
    if selected_retriever == "mmr":
        args["fetch_k"] = st.session_state["rag_fetch_k"]

    hits = qdrant_client(query=query, 
                         collection_name=selected_collection, 
                         method=SearchMethod(selected_retriever),
                         **args)
    
    st.session_state["rag_context"] = hits

def update_rag_k():
    st.session_state["rag_k"] = st.session_state["rag_k_value"]

def update_rag_fetch_k():
    st.session_state["rag_fetch_k"] = st.session_state["rag_fetch_k_value"]

### FRONTEND
st.markdown(" # :mag: Retrieval Augmented Generation (RAG)")

st.header("Input")
with st.container(border=True):
    # Selectbox displaying current options with a callback to select an option
    selected_retriever = st.selectbox("Choose a retriever", options=st.session_state["rag_options"], index=st.session_state["rag_options"].index(st.session_state["selected_rag"]))
    
    # sliders for settings
    st.slider(label="k", min_value=1, max_value=100, value=st.session_state["rag_k"], key="rag_k_value", on_change=update_rag_k)
    if selected_retriever == "mmr":
        st.slider(label="fetch_k", min_value=st.session_state["rag_k"], max_value=1000, value=st.session_state["rag_fetch_k"], key="rag_fetch_k_value", on_change=update_rag_fetch_k)

    # Text input for user to enter a new option
    st.text_input("Enter a query", key='rag_query', on_change=None)

    # Button to add the new option to the list
    st.button("Perform query", on_click=perform_query)

    st.session_state["selected_retriever"] = selected_retriever


# RAG results
if st.session_state["rag_context"] is not None:
    st.markdown("**sources**")
    for idx, doc in enumerate(st.session_state["rag_context"]):
        score = None
        if selected_retriever == "score":
            score = doc[1]
            doc = doc[0]

            st.markdown(f"**{idx+1}.({score})**")
        else:
            st.markdown(f"**{idx+1}.**")
        st.markdown(f"{doc.page_content}")