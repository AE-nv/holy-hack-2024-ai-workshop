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

        self._sim_method = SearchMethod.MMR

        self._system_prompt_template = """
            You are a chatbot that has access to transcripts of the AE Air Data Podcast. Always tell the user that you found information from the Air Data Podcast. Here is the context that was found with RAG when searching for the user's question:
            <context>
            {rag_context}
            <context>
        """
    def __call__(self, chat_history : List, collection_name : str):
        """
        """
        return self.semantic_layer(chat_history, collection_name)

    def semantic_layer(self, chat_history : List, collection_name : str):
        """
        """

        last_user_message = chat_history[-1]['content']

        route = self._dl(last_user_message)
        print(route)
        if route.name == "chitchat":
            return self._chitchat_completion(last_user_message)
        elif route.name == "airdata_rag":
            return self._rag_completion(last_user_message, collection_name)
        
        else:
            return self._nonsense(last_user_message)


    def _nonsense(self, chat_history : str):
        """
        """
        return "That does not seem relevant to me", None
    
    def _chitchat_completion(self, chat_history : str):
        """
        """
        return self._chat_model.invoke(chat_history).content, None
    
    def _rag_completion(self, chat_history : str, collection_name : str):
        """
        """

        # perform RAG
        hits = self._vectordb(chat_history, collection_name, self._sim_method)

        # call completion with context from hits
        context = "\n".join([doc.page_content for doc in hits])
        messages = [
            SystemMessage(content=self._system_prompt_template.format(rag_context=context)),
            HumanMessage(content=chat_history)
        ]
        resp = self._chat_model.invoke(messages)

        return resp.content, hits
     
