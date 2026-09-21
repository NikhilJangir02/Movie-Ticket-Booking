import requests
from django.shortcuts import render


# Create your views here.
FASTAPI_URL = "http://127.0.0.1:8000"

def movie_list(request):

    search = request.GET.get("search", "")
    genre = request.GET.get("genre", "")


    try:
        response = requests.get(f"{FASTAPI_URL}/movies")

        if response.status_code == 200:
            movies = response.json()
            print("Movies received:")
            for movie in movies:
                movie["id"] = movie.pop("_id")
        else:
            movies = []

    except Exception:
        movies = []

    if search:
        movies = [
            movie for movie in movies
            if search.lower() in movie["title"].lower()
        ]

    if genre:
        movies = [
            movie for movie in movies
            if movie["genre"] == genre
        ]

    genres = sorted(list(set(movie["genre"] for movie in movies)))  

        

    return render(
        request,
        "movies/movie_list.html",
        {
            "movies": movies,
            "genres": genres,
            "search": search,
            "selected_genre": genre
        }
    )  

       

def movie_detail(request, movie_id):

    movie_response = requests.get(
        f"{FASTAPI_URL}/movies/{movie_id}"
    )

    theater_response = requests.get(
        f"{FASTAPI_URL}/theaters/movie/{movie_id}"
    )

    if movie_response.status_code != 200:
        return render(
            request,
            "movies/not_found.html"
        )

    movie = movie_response.json()
    movie["id"] = movie.pop("_id")

    theaters = []

    if theater_response.status_code == 200:
        theaters = theater_response.json()

        for theater in theaters:
            theater["id"] = theater.pop("_id")

    return render(
        request,
        "movies/movie_detail.html",
        {
            "movie": movie,
            "theaters":theaters
        }
    )

    