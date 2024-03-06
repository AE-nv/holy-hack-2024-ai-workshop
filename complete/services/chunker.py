# services/chunker.py
# Split text files to store into vectorDb with embeddings

from typing import List
from langchain_core.documents.base import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import AzureOpenAIEmbeddings


def default_splitter(text : str, chunk_size : int = 150, chunk_overlap : int = 50):
    """
    :param text_files: List of paths to files
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    docs = text_splitter.create_documents([text])

    return docs



def semantic_splitter(text : str, embedding_function : AzureOpenAIEmbeddings):
    """

    """

    text_splitter = SemanticChunker(embedding_function)

    docs = text_splitter.create_documents([text])

    return docs



