from langchain_community.vectorstores.qdrant import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List
from enum import Enum
from langchain_core.documents.base import Document

QDRANT_URL = "http://localhost"
QDRANT_PORT = "6333"

class SearchMethod(Enum):
    SCORE = 0
    MMR = 1

class QDrantCustomClient:

    def __init__(self, collection_name, embedding_function) -> None:
        """
            Initialize QDrant client
        """
        self._client = QdrantClient(url=QDRANT_URL, port=QDRANT_PORT)

        self._qdrant = Qdrant(self._client, collection_name, embedding_function)

        self._collection_name = collection_name
        if collection_name not in self.get_collections():
            self.create_collection(collection_name=collection_name)

        
        
    def __call__(self, query : str, collection_name : str, method : SearchMethod = SearchMethod.MMR):
        """
            Perform similarity search on QDrant Vector DB
        """

        self._qdrant.collection_name = collection_name

        if method == SearchMethod.MMR:
            return self._mmr(query)
        
        elif method == SearchMethod.SCORE:
            return self._score(query)
        
        else:
            return self._simsearch(query)
           

    def add_documents(self, docs : List[Document], collection_name : str = None):
        """
        """
        if collection_name is None:
            collection_name = self._collection_name

        self._qdrant.collection_name = collection_name
         # check if collection name already exists
        if collection_name not in self.get_collections():
            self.create_collection(collection_name=collection_name)

        doc_ids = self._qdrant.add_documents(docs)

        return doc_ids



    def _mmr(self, query : str, k : int = 4, fetch_k : int = 10):
        """
        """

        found_docs = self._qdrant.max_marginal_relevance_search(query, k=k, fetch_k=fetch_k)
    
        return found_docs
    

    def _score(self, query : str, k : int = 4):
        """
        """

        found_docs = self._qdrant.similarity_search_with_score(query, k=k)

        return found_docs
    
    def _simsearch(self, query : str, k : int = 4):
        """
        """

        found_docs = self._qdrant.similarity_search(query, k=k)

        return found_docs
    
    
    def create_collection(self, collection_name : str):
        """
        """

        # check if collection name already exists
        if collection_name not in self.get_collections():
            self._client.create_collection(
                    collection_name=collection_name,
                    vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
            )
        else:
            print(f"Collection: {collection_name} already exists")


    def get_collections(self):
        """
        """
        collectionResponse = self._client.get_collections()

        return list(set([collection.name for collection in collectionResponse.collections]))

    def delete_collections(self):
        """
        """
        
        collections = self.get_collections()
        for collection in collections:
            self._client.delete_collection(collection_name=collection)
    
    def delete_collection(self, collection_name : str):
        """
        """

        if collection_name in self.get_collections():
            self._client.delete_collection(collection_name=collection_name)
        else: 
            print("No collection by that name")

    def get_collection_details(self, collection_name):
        """
        """

        coll = self._client.get_collection(collection_name)

        vectorcount = coll.vectors_count
        return {'vector_count' : vectorcount}

        

