from st_pages import show_pages_from_config, add_page_title
import streamlit as st
import os
from services import transcribe, default_splitter, semantic_splitter
from dotenv import load_dotenv
from Home import init_qdrantdb

st.set_page_config(page_title="Upload Data",
                   page_icon=":books:",
                   layout="wide")

load_dotenv()  # take environment variables from .env.


# ChromaDB connection --> should be cached
if "qdrant_client" in st.session_state:
    qdrant_client = st.session_state["qdrant_client"]
else:
    qdrant_client = init_qdrantdb()
    st.session_state["qdrant_client"] = qdrant_client

# collection selections
st.session_state["collection_options"] = qdrant_client.get_collections()



if len(st.session_state["collection_options"]) == 0:
    qdrant_client.create_collection(qdrant_client._collection_name)
    st.session_state["collection_options"] = qdrant_client.get_collections()

if 'selected_collection' not in st.session_state:
    st.session_state["selected_collection"] = st.session_state["collection_options"][0]

def add_collection():
    option = st.session_state["new_collection_name"]
    if option and option not in st.session_state["collection_options"]:
        st.session_state["collection_options"].append(option)
        st.session_state["new_collection_name"] = ''  # Reset the input field
        st.session_state["selected_collection"] = option
        qdrant_client.create_collection(option)

# Function to remove the selected option from the options list
def remove_collection():
    st.session_state['collection_options'].remove(st.session_state['selected_collection'])
    qdrant_client.delete_collection(st.session_state['selected_collection'])
 
def upload_files():
    files = st.session_state["uploaded_files"]

    for file in files:
        print("processing file: ", file)
        # if files are not txt, but audio, check that size is less than 25MB
        filename = file.name
        name, ext = os.path.splitext(filename)
        ext = ext.replace('.', '')
        if ext in ['mp3', 'mp4', 'wav']:
            file_size = file.size
            if file_size / 1e6 < 25:
                # transcribe mp3 file
                transcript = transcribe(file)

                # save transcript to folder
                transcript_folder = os.path.join(os.getenv("LOCAL_DATA_FOLDER"), "transcripts")
                print(transcript_folder)
                os.makedirs(transcript_folder, exist_ok=True)
                with open(os.path.join(transcript_folder, f"{name}.txt"), "w") as f:
                    f.write(transcript)
                
                # split transcript
                if selected_splitter == "recursive_text":
                    docs = default_splitter(transcript)
                elif selected_splitter == "semantic":
                    docs = semantic_splitter(transcript, qdrant_client._qdrant.embeddings)
            
                # add chunks to vectordb
                doc_ids = qdrant_client.add_documents(docs, st.session_state["selected_collection"])
                

            else: # should show warning
                print(f"Cannot use files with extension '{ext}' with size bigger than 25MB.")
        
        else: # should be .txt file
            file_bytes = file.getvalue()

            transcript = file_bytes.decode(errors='replace')

            print(selected_splitter)
             # split transcript
            if selected_splitter == "recursive text":
                docs = default_splitter(transcript)
            elif selected_splitter == "semantic":
                docs = semantic_splitter(transcript, qdrant_client._qdrant.embeddings)
            
            # add chunks to vectordb
            doc_ids = qdrant_client.add_documents(docs, st.session_state["selected_collection"])
            

st.markdown(" # :books: Upload Data")

# upload files 
st.header("1.File upload")
with st.container(border=True):
    files = st.file_uploader("Air Data files", accept_multiple_files=True, key="uploaded_files")

    st.button("Upload files to collection", on_click=upload_files)

# select splitter function
st.header("2.Splitter")
with st.container(border=True): 
    selected_splitter = st.selectbox("Splitter function", ["recursive text", "semantic"])

st.header("3.Collection")
with st.container(border=True):
    # Text input for user to enter a new option
    st.text_input("Enter new collection Name", key='new_collection_name', on_change=None)

    # Button to add the new option to the list
    st.button("Add Collection", on_click=add_collection)

    # Selectbox displaying current options with a callback to select an option
    selected_collection = st.selectbox("Choose a collection", options=st.session_state["collection_options"], index=st.session_state["collection_options"].index(st.session_state["selected_collection"]))
    st.session_state["selected_collection"] = selected_collection
    st.text(qdrant_client.get_collection_details(st.session_state['selected_collection']))

    # Button to remove the selected option from the list
    st.button("Remove Selected collectionn", on_click=remove_collection)

