import requests
from langchain_core.documents import Document
from database.connect_to_database import connect_to_database
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

# =========================
# 🛠️ TMDB API İŞLEMLERİ
# =========================

def fetch_genres():
    url = f"{BASE_URL}/genre/movie/list"
    params = {"api_key": API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)
    return response.json().get("genres", [])

def fetch_movies(page=1):
    url = f"{BASE_URL}/movie/popular"
    params = {"api_key": API_KEY, "language": "en-US", "page": page}
    response = requests.get(url, params=params)
    return response.json().get("results", [])

# =========================
# 💾 MYSQL
# =========================

def save_to_mysql(movies, genres):
    conn = connect_to_database()
    if not conn: return
    cursor = conn.cursor()

    try:
        genre_sql = "INSERT IGNORE INTO genres (id, name) VALUES (%s, %s)"
        genre_data = [(g['id'], g['name']) for g in genres]
        cursor.executemany(genre_sql, genre_data)

        movie_sql = """
            INSERT INTO movies (id, title, overview, release_year, rating, popularity)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            rating = VALUES(rating), popularity = VALUES(popularity)
        """
        rel_sql = "INSERT IGNORE INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)"

        movie_entries = []
        relation_entries = []

        for m in movies:
            release_date = m.get("release_date", "")
            year = int(release_date[:4]) if release_date else None
            
            movie_entries.append((
                m['id'], m['title'], m['overview'], year, 
                m['vote_average'], m['popularity']
            ))

            for g_id in m.get("genre_ids", []):
                relation_entries.append((m['id'], g_id))

        cursor.executemany(movie_sql, movie_entries)
        cursor.executemany(rel_sql, relation_entries)

        conn.commit()

    except Exception as e:
        print(f"❌ MySQL Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# =========================
# 🧱 VECTOR DB
# =========================

def tmdb_to_documents(movies, genre_list):
    genre_map = {g['id']: g['name'] for g in genre_list}
    documents = []
    ids = []
    seen_ids = set()
    
    for m in movies:
        movie_id = str(m.get("id"))
        
        if movie_id in seen_ids:
            continue
        
        seen_ids.add(movie_id)
        
        title = m.get("title", "")
        overview = m.get("overview", "")
        genre_names = [genre_map.get(gid, "Unknown") for gid in m.get("genre_ids", [])]
        
        doc = Document(
            page_content=f"Movie: {title}\nPlot: {overview}\nGenres: {', '.join(genre_names)}",
            metadata={
                "title": title,
                "year": m.get("release_date", "")[:4],
                "rating": m.get("vote_average"),
                "genres": genre_names
            }
        )
        documents.append(doc)
        ids.append(movie_id)
        
    return documents, ids

def load_all_data(pages=10):
    genres = fetch_genres()
    all_movies = []

    for p in range(1, pages + 1):
        print(f"🌐 Page {p} is loading...")
        all_movies.extend(fetch_movies(p))

    save_to_mysql(all_movies, genres)

    return tmdb_to_documents(all_movies, genres)
load_movies = load_all_data