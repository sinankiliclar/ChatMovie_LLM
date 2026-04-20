import pymysql
from langchain_core.documents import Document
from dotenv import load_dotenv
import os

load_dotenv()

def load_movies_from_mysql():
    db = None
    try:
        db = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 3306)),
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with db.cursor() as cursor:
            query = """
            SELECT 
                m.id, 
                m.title, 
                m.overview, 
                m.release_year, 
                m.rating, 
                m.popularity,
                GROUP_CONCAT(g.name SEPARATOR ', ') as genre_names
            FROM movies m
            LEFT JOIN movie_genres mg ON m.id = mg.movie_id
            LEFT JOIN genre g ON mg.genre_id = g.id
            GROUP BY m.id;
            """
            
            cursor.execute(query)
            rows = cursor.fetchall()

            documents = []
            ids = []

            for row in rows:
                content = f"""Movie: {row['title']}
Plot: {row['overview']}
Release Year: {row['release_year']}
Rating: {row['rating']}
Genres: {row['genre_names'] if row['genre_names'] else 'N/A'}"""

                doc = Document(
                    page_content=content,
                    metadata={
                        "title": row['title'],
                        "year": row['release_year'],
                        "rating": float(row['rating']) if row['rating'] else 0.0,
                        "popularity": float(row['popularity']) if row['popularity'] else 0.0,
                        "genres": row['genre_names']
                    }
                )
                documents.append(doc)
                ids.append(str(row['id']))

            return documents, ids

    except pymysql.MySQLError as err:
        print(f"❌ PyMySQL Error: {err}")
        return [], []
    
    finally:
        if db:
            db.close()