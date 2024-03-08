#services/chat.py

from semantic_router import Route
from semantic_router.encoders.zure import AzureOpenAIEncoder
from semantic_router.layer import RouteLayer
from .vectordb import QDrantCustomClient, SearchMethod
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

import os
from typing import List

class SemanticRouter:
    """
    add description and link to github page
    
    """
    def __init__(self, vectordb : QDrantCustomClient) -> None:

        self._vectordb = vectordb
        self._encoder = AzureOpenAIEncoder(azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                             api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                             api_version="2023-05-15",
                             model="text-embedding-ada-002",
                             deployment_name="ada-002")
        
        self._chat_model = AzureChatOpenAI(azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                                           api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                                           api_version="2023-05-15",
                                           model="gpt-35-turbo")
        
        print("Not Implemented yet.")
        
        # define routes

        # create route layer

        # define system prompt
        self._system_prompt_template = """
            TODO: write a system prompt
        """
        
    def __call__(self, query : List, collection_name : str, **kwargs):
        """
        Call the semantic_layer function to semantically reroute the user query 
        """
        return self.semantic_layer(query, collection_name, **kwargs)

    def semantic_layer(self, query : List, collection_name : str, **kwargs):
        """
        TODO: Reroute the user query and call the routed completion functions
        """
        print("Not Implemented yet.")

    
    def _nonsense(self, chat_history : str):
        """
        Route: Nonsense (default)
        Respond to nonsense route 
        :chat_history(string) : The user query

        :returns: response, rag_context(None) 
        """
        return "That does not seem relevant to me", None
    
    def _chitchat_completion(self, query : str):
        """
        Route: greetings
        Respond to greetings route 
        :chat_history(string) : The user query

        :returns: response, rag_context(None) 
        """
        print("Not Implemented yet.")
    
    def _rag_completion(self, query : str, collection_name : str, **kwargs):
        """
        Route: Air Data relevant query - Solve with RAG
        Respond to airdata_rag route 
        :chat_history(string) : The user query
        :collection_name (string) : The collection of VectorDB to use for RAG
        :**kwargs (Dict) : The parameters for the VectorDB retriever

        :returns: response, rag_context
        """

        print("Not Implemented yet.")
     
