import requests
from django.shortcuts import render, redirect
from users.utils import get_auth_headers
from users.decorators import admin_required

# Create your views here.
FASTAPI_URL = "http://127.0.0.1:8000"


@admin_required
def dashboard(request):
    
    return render(request, "dashboard/dashboard.html")



@admin_required
def add_movie(request):

    if request.method == "POST":
        print(request.POST)

        data = {
            "title": request.POST.get("title"),
            "description": request.POST.get("description"),
            "genre": request.POST.get('genre'),
            "language": request.POST.get("language"),
            "duration": int(request.POST.get("duration")),
            "release_year": int(request.POST.get("release_year")),
            "rating": float(request.POST.get("rating")),
            "poster_url": request.POST.get("poster_url")
        }

        response = requests.post(
            f"{FASTAPI_URL}/movies/",
            json=data,
            headers=get_auth_headers(request)
        )

        if response.status_code == 401:
            request.session.flush()
            return redirect("login")
        

        if response.status_code == 200:
            return redirect("dashboard")

        return render(
            request,
            "dashboard/add_movie.html",
            {"error": response.json()}
        )

    return render(request, "dashboard/add_movie.html")



@admin_required
def manage_movies(request):

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
        "dashboard/manage_movies.html",
        {
            "movies": movies
        }
    )        



@admin_required
def edit_movie(request, movie_id):


    response = requests.get(
        f"{FASTAPI_URL}/movies/{movie_id}"
    )

    if response.status_code != 200:
        return redirect("manage_movies")

    movie = response.json()

    if request.method == "POST":

        data = {
            "title": request.POST.get("title"),
            "description": request.POST.get("description"),
            "genre": request.POST.get("genre"),
            "language": request.POST.get("language"),
            "duration": int(request.POST.get("duration")),
            "release_year": int(request.POST.get("release_year")),
            "rating":float(request.POST.get("rating")),
            "poster_url": request.POST.get("poster_url")

        }

        response = requests.put(
            f"{FASTAPI_URL}/movies/{movie_id}",
            json=data,
            headers=get_auth_headers(request)
        )

        if response.status_code == 401:
            request.session.flush()
            return redirect("login")
        

        if response.status_code == 200:
            return redirect("manage_movies")

        return render(
            request,
            "dashboard/edit_movie.html",
            {
                "movie": movie,
                "error": response.json()
            }
        )

    return render(
        request,
        "dashboard/edit_movie.html",
        {
            "movie": movie
        }
    )




@admin_required
def delete_movie(request, movie_id):


    response = requests.delete(
        f"{FASTAPI_URL}/movies/{movie_id}",
        headers=get_auth_headers(request)
    )

    if response.status_code == 401:
        request.session.flush()
        return redirect("login")
    

    return redirect("manage_movies")


@admin_required
def manage_theaters(request):


    response = requests.get(
        f"{FASTAPI_URL}/theaters/"
    )

    theaters = []

    if  response.status_code == 200:
        theaters = response.json()

        for theater in theaters:
            theater["id"] = theater.pop("_id")

    return render(
        request,
        "dashboard/manage_theaters.html",
        {
            "theaters": theaters
        }
    ) 

@admin_required
def add_theater(request):

    movies_response = requests.get(
        f"{FASTAPI_URL}/movies/"
    )

    movies = []

    if movies_response.status_code == 200:
        movies = movies_response.json()

        for movie in movies:
            movie["id"] = movie.pop("_id")

    if request.method == "POST":

        data = {
            "name": request.POST.get("name"),
            "city": request.POST.get("city"),
            "address": request.POST.get("address"),
            "total_seats": int(request.POST.get("total_seats")),
            "movie_id": request.POST.get("movie_id")
        }

        response = requests.post(
            f"{FASTAPI_URL}/theaters/",
            json=data,
            headers=get_auth_headers(request)
        )

        if response.status_code == 401:
            request.session.flush()
            return redirect("login")

        if response.status_code == 200:
            return redirect("manage_theaters")

        return render(
            request,
            "dashboard/add_theater.html",
            {
                "movies": movies,
                "error": response.json()
            }
        )

    return render(
        request,
        "dashboard/add_theater.html",
        {
            "movies": movies
        }
    )


@admin_required
def edit_theater(request, theater_id):

    response = requests.get(
        f"{FASTAPI_URL}/theaters/{theater_id}"
    )

    if response.status_code != 200:
        return redirect("manage_theaters")

    theater = response.json()

    movies = requests.get(
        f"{FASTAPI_URL}/movies/"
    ).json()

    for movie in movies:
        movie["id"] = movie.pop("_id")

    if request.method == "POST":

        data = {
            "name": request.POST.get("name"),
            "city": request.POST.get("city"),
            "address": request.POST.get("address"),
            "total_seats": int(request.POST.get("total_seats")),
            "movie_id": request.POST.get("movie_id")
        }

        response = requests.put(
            f"{FASTAPI_URL}/theaters/{theater_id}",
            json=data,
            headers=get_auth_headers(request)
        )

        if response.status_code == 401:
            request.session.flush()
            return redirect("login")

        if response.status_code == 200:
            return redirect("manage_theaters")

    return render(
        request,
        "dashboard/edit_theater.html",
        {
            "theater": theater,
            "movies": movies
        }
    )

@admin_required
def delete_theater(request, theater_id):

    response = requests.delete(
        f"{FASTAPI_URL}/theaters/{theater_id}",
        headers=get_auth_headers(request)
    )

    if response.status_code == 401:
        request.session.flush()
        return redirect("login")

    return redirect("manage_theaters")



@admin_required
def manage_shows(request):

    response = requests.get(
        f"{FASTAPI_URL}/shows/",
    )

    shows = []

    if response.status_code == 200:

        shows = response.json()

        for show in shows:
            show["id"] = show.pop("_id")

    return render(
        request,
        "dashboard/manage_shows.html",
        {
            "shows": shows
        }
    )      



@admin_required
def add_show(request):

    movies = requests.get(
        f"{FASTAPI_URL}/movies/"
    ).json()

    for movie in movies:
        movie["id"] = movie.pop("_id")

    theaters = requests.get(
        f"{FASTAPI_URL}/theaters/"
    ).json()

    for theater in theaters:
        theater["id"] = theater.pop("_id")

    if request.method == "POST":

        data = {
            "movie_id": request.POST.get("movie_id"),
            "theater_id": request.POST.get("theater_id"),
            "show_date": request.POST.get("show_date"),
            "show_time": request.POST.get("show_time"),
            "price": float(request.POST.get("price"))
        }

        response = requests.post(
            f"{FASTAPI_URL}/shows/",
            json=data,
            headers=get_auth_headers(request)
        )

        if response.status_code == 401:
            request.session.flush()
            return redirect("login")
        

        if response.status_code == 200:
            return redirect("manage_shows")

        return render(
            request,
            "dashboard/add_show.html",
            {
                "movies": movies,
                "theaters": theaters,
                "error": response.json()
            }
        )
        

    return render(
        request,
        "dashboard/add_show.html",
        {
            "movies": movies,
            "theaters": theaters
        }

    )



@admin_required
def edit_show(request, show_id):

    show_response = requests.get(
        f"{FASTAPI_URL}/shows/{show_id}"
    )

    if show_response.status_code != 200:
        return redirect("manage_shows")

    show = show_response.json()

    movies = requests.get(
        f"{FASTAPI_URL}/movies/"
    ).json()

    theaters = requests.get(
        f"{FASTAPI_URL}/theaters/"
    ).json()

    if request.method == "POST":

        data = {
            "movie_id": request.POST.get("movie_id"),
            "theater_id": request.POST.get("theater_id"),
            "show_date": request.POST.get("show_date"),
            "show_time": request.POST.get("show_time"),
            "price": float(request.POST.get("price"))
        }

        response = requests.put(
            f"{FASTAPI_URL}/shows/{show_id}",
            json=data,
            headers=get_auth_headers(request)
        )

        if response.status_code == 401:
            request.session.flush()
            return redirect("login")
        


        if response.status_code == 200:
            return redirect("manage_shows")

    return render(
        request,
        "dashboard/edit_show.html",
        {
            "show": show,
            "movies": movies,
            "theaters": theaters
        }
    )    


@admin_required
def delete_show(request, show_id):


    response = requests.delete(
        f"{FASTAPI_URL}/shows/{show_id}",
        headers=get_auth_headers(request)
    )

    if response.status_code == 401:
        request.session.flush()
        return redirect("login")
    
    
    return redirect("manage_shows")




@admin_required
def movie_shows(request, movie_id):

    movie_response = requests.get(
        f"{FASTAPI_URL}/movies/{movie_id}"
    )

    show_response = requests.get(
        f"{FASTAPI_URL}/shows/movie/{movie_id}"
    )

    if movie_response.status_code != 200:
        return redirect("home")

    movie = movie_response.json()

    shows = []

    if show_response.status_code == 200:
        shows = show_response.json()

        for  show in  shows:
            show["id"] = show.pop("_id")

    return render(
        request,
        "dashboard/movie_shows.html",
        {
            "movie": movie,
            "shows": shows
        }
    )        



@admin_required
def book_show(request, show_id):

    show_response = requests.get(
        f"{FASTAPI_URL}/shows/{show_id}"
    )

    if show_response.status_code != 200:
        return redirect("manage_shows")

    show = show_response.json()

    if request.method == "POST":

        data = {
            "show_id": show_id,
            "seats": int(request.POST.get("seats"))
        }

        response = requests.post(
            f"{FASTAPI_URL}/booking/",
            json=data,
            headers=get_auth_headers(request)
        )

        if response.status_code == 401:
            request.session.flush()
            return redirect("login")
        

        if response.status_code == 200:
            return redirect("my_bookings")

        return render(
            request,
            "dashboard/book_show.html",
            {
                "show": show,
                "error": response.json()
            }
        )

    return render(
        request,
        "dashboard/book_show.html",
        {
            "show": show
        }
    )            
