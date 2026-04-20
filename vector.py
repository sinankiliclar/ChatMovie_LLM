from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

df = pd.read_csv("movies.csv")
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "./chroma_movie_db"
add_documents = not os.path.exists(db_location)

if add_documents:
    documents = []
    ids = []
    
    for i, row in df.iterrows():
        
        document = Document(
            
            page_content=f"Film: {row['Title']}\nKonu: {row['Plot']}", 
            
            metadata={
                "title": row["Title"], 
                "genre": row["Genre"], 
                "director": row["Director"],
                "year": row["Year"],
                "rating": row["Rating"]
            },
            id=str(i)
        )
        ids.append(str(i))
        documents.append(document)
        
vector_store = Chroma(
    collection_name="movie_database",
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)
    
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)