from langchain_community.vectorstores.qdrant import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List
from enum import Enum
from langchain_core.documents.base import Document

QDRANT_URL = "http://localhost"
QDRANT_PORT = "6333"

class SearchMethod(Enum):
    SCORE = "score"
    SIMSEARCH = "simsearch"
    MMR = "mmr"
    """
    Enum for search methods. SCORE for simple scoring, MMR for Maximal Marginal Relevance.
    """

class QDrantCustomClient:
    """
    A custom client for interfacing with Qdrant, a vector search engine. This client abstracts
    some of the operations on collections and documents, allowing for simplified document management
    and search functionalities.
    """

    def __init__(self, collection_name, embedding_function) -> None:
        """
        Initializes a new instance of the QDrantCustomClient class.

        Args:
            collection_name (str): The name of the collection to operate on.
            embedding_function: A function that generates embeddings from documents.
        """
        self._client = QdrantClient(url=QDRANT_URL, port=QDRANT_PORT)

        self._qdrant = Qdrant(self._client, collection_name, embedding_function)

        self._collection_name = collection_name
        if collection_name not in self.get_collections():
            self.create_collection(collection_name=collection_name)

        
        
    def __call__(self, query : str, collection_name : str, method : SearchMethod = SearchMethod.MMR):
        """
        Performs a similarity search on a Qdrant Vector DB using the specified search method.

        Args:
            query (str): The search query.
            collection_name (str): The name of the collection to search in.
            method (SearchMethod): The search method to use. Defaults to MMR.

        Returns:
            The search results.
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
        Adds documents to the specified collection.

        Args:
            docs (List[Document]): A list of documents to add.
            collection_name (str, optional): The name of the collection. Defaults to the initialized collection name.

        Returns:
            The IDs of the added documents.
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
        TODO: Performs a Maximal Marginal Relevance (MMR) search.

        Args:
            query (str): The search query.
            k (int): The number of results to return.
            fetch_k (int): The number of results to fetch for relevance calculation.

        Returns:
            The search results.
        """

        print("Not Implemented yet.")
    

    def _score(self, query : str, k : int = 4):
        """
        TODO: Performs a similarity search returning the scores as well

        Args:
            query (str): The search query.
            k (int): The number of results to return.

        Returns:
            The search results.
        """

        print("Not Implemented yet.")

    
    def _simsearch(self, query : str, k : int = 4):
        """
        TODO: Performs a basic similarity search

        Args:
            query (str): The search query.
            k (int): The number of results to return.

        Returns:
            The search results.
        """

        print("Not Implemented yet.")
    
    
    def create_collection(self, collection_name : str):
        """
        Creates a new collection with the specified name if it doesn't already exist.

        Args:
            collection_name (str): The name of the collection to create.
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
        Retrieves a list of all collection names.

        Returns:
            A list of collection names.
        """
        collectionResponse = self._client.get_collections()

        return list(set([collection.name for collection in collectionResponse.collections]))

    def delete_collections(self):
        """
        Deletes all collections managed by this client.
        """
        
        collections = self.get_collections()
        for collection in collections:
            self._client.delete_collection(collection_name=collection)
    
    def delete_collection(self, collection_name : str):
        """
        Deletes a specific collection by name.

        Args:
            collection_name (str): The name of the collection to delete.
        """

        if collection_name in self.get_collections():
            self._client.delete_collection(collection_name=collection_name)
        else: 
            print("No collection by that name")

    def get_collection_details(self, collection_name):
        """
        Retrieves details for a specific collection.

        Args:
            collection_name (str): The name of the collection.

        Returns:
            A dictionary containing details of the collection, such as vector count.
        """

        coll = self._client.get_collection(collection_name)

        vectorcount = coll.vectors_count
        return {'vector_count' : vectorcount}

        

