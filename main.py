from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
import os

from data_loader import load_movies_from_mysql
from vector_store import create_or_load_vector_store

# =========================
# 🧠 MODEL
# =========================
model = OllamaLLM(model="llama3.2")

template = """You are ChatMovie, an expert in cinema.

Use the movie information below to answer the user's question.

Only use conversation history if it is directly relevant to the question. Otherwise, ignore it.

Only recommend movies that exist in the provided movie information. Do not make up movies.

Movie information:
{reviews}

Conversation history:
{chat_history}

User question:
{question}

Give a clear and natural answer. Do NOT mention the conversation history unless necessary.
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# =========================
# 💬 MEMORY
# =========================
chat_history = []

# =========================
# 🧱 1. DB BUILD
# =========================
if not os.path.exists("./chroma_movie_db"):
    documents, ids = load_movies_from_mysql()
    
    if documents:
        vector_store = create_or_load_vector_store(documents, ids)
    else:
        exit()
else:
    vector_store = create_or_load_vector_store()
retriever = vector_store.as_retriever(search_kwargs={"k": 5})

print("📦 Total movies in DB:", vector_store._collection.count())

# =========================
# 🔁 CHAT LOOP
# =========================
while True:
    print("\n-------------------------------")
    question = input("Ask your question about movies (q to quit): ")

    if question.lower() == "q":
        break

    # 🔍 RETRIEVAL
    docs = retriever.invoke(question)

    reviews = "\n\n".join([
        f"{d.metadata.get('title','')}: {d.page_content}"
        for d in docs
    ])

    history_text = "\n".join([
        f"User: {m.content}" if isinstance(m, HumanMessage)
        else f"Assistant: {m.content}"
        for m in chat_history
    ])

    # 🤖 LLM
    result = chain.invoke({
        "reviews": reviews,
        "question": question,
        "chat_history": history_text
    })

    print("\n🎬 ChatMovie:", result)

    # 💾 MEMORY
    chat_history.append(HumanMessage(content=question))
    chat_history.append(AIMessage(content=result))

    if len(chat_history) > 6:
        chat_history = chat_history[-6:]