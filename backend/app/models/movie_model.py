from datetime import datetime

def movie_document(movie):

    return {
        "title": movie.title,
        "description": movie.description,
        "genre": movie.genre,
        "language": movie.language,
        "duration": movie.duration,
        "release_year": movie.release_year,
        "rating": movie.rating,
        "poster_url": movie.poster_url,
        "created_at": datetime.utcnow()
    }