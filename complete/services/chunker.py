# services/chunker.py
# Split text files to store into vectorDb with embeddings

from typing import List
from langchain_core.documents.base import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import AzureOpenAIEmbeddings


def default_splitter(text : str, chunk_size : int = 150, chunk_overlap : int = 50):
    """
    Split a text using the RecursiveCharacterTextSplitter.

    :param text_files:      List of paths to files
    :param chunk_size:      The number of characters in one chunk
    :param chunk_overlap:   The overlap between two chunks
    """
    # create text splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    # split documents with text splitter
    docs = text_splitter.create_documents([text])

    return docs



def semantic_splitter(text : str, embedding_function : AzureOpenAIEmbeddings):
    """
    Split a text using the Semantic Chunker.

    :param text_files:          List of paths to files
    :param embedding_function:  AzureOpenAIEmbeddings object used to compare sentence embeddings

    """

    # create semantic chunker 
    text_splitter = SemanticChunker(embedding_function)

    # Use semantic chunker to split documents
    docs = text_splitter.create_documents([text])

    return docs



