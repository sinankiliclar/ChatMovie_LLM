import os
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

DB_PATH = "./chroma_movie_db"

def create_or_load_vector_store(documents=None, ids=None):

    embeddings = OllamaEmbeddings(model="mxbai-embed-large")

    vector_store = Chroma(
        collection_name="movie_database",
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

    count = len(vector_store.get()['ids'])
    print(f"📦 Current DB size: {count}")

    if count == 0:
        print("⚠️ DB is empty → rebuilding from TMDB...")

        if documents is None or ids is None:
            raise ValueError("No data provided to rebuild DB")

        vector_store.add_documents(documents=documents, ids=ids)

        print("✅ DB successfully rebuilt!")

    else:
        print("✅ DB already exists, skipping rebuild")

    return vector_store

def get_retriever():
    
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    
    vector_store = Chroma(
        collection_name="movie_database",
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )
    
    return vector_store.as_retriever(search_kwargs={"k": 5})