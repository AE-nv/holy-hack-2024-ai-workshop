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
        
        greetings_router = Route(
            name="chitchat",
            utterances= [
                "Hi, how are you?",
                "Hi, can you help me?"
                "What do you do?",
                "lovely weather today"
            ]
        )

        airdata_router = Route(
            name="airdata_rag",
            utterances=
            [
                "what do you know about data visualization?",
                "What did they say about pie charts?",
                "What did they talk about in this episode?",
                "Wat vinden ze van het nieuwe decor?",
                "what are the key takeaways of the air data podcast?"
            ]
        )
        self._routes = [greetings_router, airdata_router]
        
         # create route layer
        self._dl = RouteLayer(encoder=self._encoder, routes=self._routes)

        self._system_prompt_template = """
            You are a chatbot that has access to transcripts of the AE Air Data Podcast. Always tell the user that you found information from the Air Data Podcast. Here is the context that was found with RAG when searching for the user's question:
            <context>
            {rag_context}
            <context>
        """
    def __call__(self, chat_history : List, collection_name : str, **kwargs):
        """
        Call the semantic_layer function to semantically reroute the user query 
        """
        return self.semantic_layer(chat_history, collection_name, **kwargs)

    def semantic_layer(self, chat_history : List, collection_name : str, **kwargs):
        """
        Reroute the user query and call the routed completion functions
        """

        last_user_message = chat_history[-1]['content']

        route = self._dl(last_user_message)
        print(route)
        if route.name == "chitchat":
            return self._chitchat_completion(last_user_message)
        elif route.name == "airdata_rag":
            return self._rag_completion(last_user_message, collection_name, **kwargs)
        
        else:
            return self._nonsense(last_user_message)


    def _nonsense(self, chat_history : str):
        """
        Route: Nonsense (default)
        Respond to nonsense route 
        :chat_history(string) : The user query

        :returns: response, rag_context(None) 
        """
        return "That does not seem relevant to me", None
    
    def _chitchat_completion(self, chat_history : str):
        """
        Route: greetings
        Respond to greetings route 
        :chat_history(string) : The user query

        :returns: response, rag_context(None) 
        """
        return self._chat_model.invoke(chat_history).content, None
    
    def _rag_completion(self, chat_history : str, collection_name : str, **kwargs):
        """
        Route: Air Data relevant query - Solve with RAG
        Respond to airdata_rag route 
        :chat_history(string) : The user query
        :collection_name (string) : The collection of VectorDB to use for RAG
        :**kwargs (Dict) : The parameters for the VectorDB retriever

        :returns: response, rag_context
        """

        # perform RAG
        selected_method = kwargs["method"]
        kwargs.pop("method")
        hits = self._vectordb(chat_history, collection_name, method=selected_method, **kwargs)

        # call completion with context from hits
        if selected_method == SearchMethod.SCORE:
            
            context = "\n".join([doc[0].page_content for doc in hits])
        else:
            context = "\n".join([doc.page_content for doc in hits])

        messages = [
            SystemMessage(content=self._system_prompt_template.format(rag_context=context)),
            HumanMessage(content=chat_history)
        ]
        resp = self._chat_model.invoke(messages)

        return resp.content, hits
     
