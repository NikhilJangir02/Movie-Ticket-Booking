from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("movies/add/", views.add_movie, name="add_movie"),
    path("movies/", views.manage_movies, name="manage_movies"),
    path("movies/edit/<str:movie_id>/", views.edit_movie, name="edit_movie"),
    path("movies/delete/<str:movie_id>/", views.delete_movie, name="delete_movie"), 
    path("theaters/", views.manage_theaters, name="manage_theaters"),
    path("theaters/add/", views.add_theater, name="add_theater"),
    path("theaters/edit/<str:theater_id>/", views.edit_theater, name="edit_theater"),
    path("theaters/delete/<str:theater_id>/", views.delete_theater, name="delete_theater"),
    path("shows/", views.manage_shows, name="manage_shows"),
    path("shows/add/", views.add_show, name="add_show"),
    path("shows/edit/<str:show_id>/", views.edit_show, name="edit_show"),
    path("shows/delete/<str:show_id>/", views.delete_show, name="delete_show"),
    path("movie/<str:movie_id>/shows/", views.movie_shows, name="movie_shows"),
    path("shows/book/<str:show_id>/", views.book_show, name="book_show"),
]
