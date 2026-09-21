import requests
from django.shortcuts import render

# Create your views here.
FASTAPI_URL = "http://127.0.0.1:8000"

def home(request):
    response = requests.get(
        f"{FASTAPI_URL}/movies/"
    )

    movies = []

    if response.status_code == 200:
        movies = response.json()


        for movie in movies:
            movie["id"] = movie.pop("_id")

    return render(
        request,
        "home/index.html",
        {
            "movies": movies
        }
    )        