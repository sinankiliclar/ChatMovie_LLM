# 🎬 ChatMovie – AI Movie Recommendation Chatbot

ChatMovie is a **Retrieval-Augmented Generation (RAG)** based movie chatbot that uses **LLMs + Vector Search** to provide accurate and context-aware movie recommendations.

---

## 🚀 Features

* 🔍 Semantic movie search with **ChromaDB**
* 🧠 AI responses using **Ollama (Llama 3)**
* 💾 Structured storage with **MySQL**
* 🌐 Live data from **TMDB API**
* 💬 Conversation memory support
* ❌ No hallucinated movies (only DB-backed answers)

---

## 🏗️ Architecture

```text
TMDB API → MySQL → ChromaDB → LLM → User
```

* **TMDB** → Fetches movie data
* **MySQL** → Stores structured data
* **ChromaDB** → Vector search (semantic retrieval)
* **LLM (Ollama)** → Generates final answers

---

## 🛠️ Tech Stack

* Python
* LangChain
* Ollama
* ChromaDB
* MySQL
* TMDB API

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/sinankiliclar/ChatMovie_LLM.git
cd chatmovie
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Create `.env` file

Copy the example:

```bash
cp .env.example .env
```

Fill in your credentials:

```env
TMDB_API_KEY=your_api_key
DB_PASSWORD=your_mysql_password
```

---

### 4. Setup MySQL

Run:

```bash
mysql -u root -p < schema.sql
```

---

### 5. Load movie data

```python
from tmdb import load_all_data

load_all_data()
```

---

### 6. Run the chatbot

```bash
python main.py
```

---

## 💡 Example Usage

```text
Ask your question about movies:
> Recommend me sci-fi movies with high ratings

🎬 ChatMovie:
Here are some highly rated sci-fi movies...
```

---

## 🔄 How It Works

1. User asks a question
2. Query is converted into embeddings
3. ChromaDB retrieves relevant movies
4. Context is sent to LLM
5. LLM generates grounded answer

---

## 🔐 Environment Variables

| Variable     | Description    |
| ------------ | -------------- |
| TMDB_API_KEY | TMDB API key   |
| DB_HOST      | Database host  |
| DB_USER      | MySQL username |
| DB_PASSWORD  | MySQL password |
| DB_NAME      | Database name  |

---

## ⚠️ Important Notes

* `.env` file is **not included** for security reasons
* Never commit API keys or passwords
* First run may take time (vector DB creation)
* If new movies are added → rebuild ChromaDB

---

## 🚀 Future Improvements

* 🎯 Advanced filtering (genre, rating, year)
* ⚡ Faster retrieval with re-ranking
* 🌐 Web UI (Streamlit / React)
* 🔌 API layer (FastAPI)
* 🔄 Auto-sync with TMDB

---

## 📄 License

MIT License
