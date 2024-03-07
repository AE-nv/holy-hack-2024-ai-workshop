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

        # define default search method

        # define system prompt
        self._system_prompt_template = """
            TODO: write a system prompt
        """
        
    def __call__(self, query : List, collection_name : str):
        """
        Calls the semantic_layer function to semantically reroute the user query 
        """
        return self.semantic_layer(query, collection_name)

    def semantic_layer(self, query : List, collection_name : str):
        """
        TODO: Reroute the user query and call the routed completion functions
        """
        print("Not Implemented yet.")

    
    def _chitchat_completion(self, query : str):
        """
        Route: greetings
        """
        print("Not Implemented yet.")
    
    def _rag_completion(self, query : str, collection_name : str):
        """
        Route: Air Data relevant query - Solve with RAG
        """

        print("Not Implemented yet.")
     
