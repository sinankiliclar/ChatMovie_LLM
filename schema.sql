CREATE DATABASE movie_db;

USE movie_db;

CREATE TABLE movies (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    overview TEXT,
    release_year INT,
    rating FLOAT,
    popularity FLOAT
);

CREATE TABLE genres (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE movie_genres (
    movie_id INT,
    genre_id INT,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (genre_id) REFERENCES genres(id)
);