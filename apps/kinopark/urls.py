from django.urls import re_path, path
from apps.kinopark import views

urlpatterns = [
    re_path(r'api/kinopark/films$', views.movies_list),
    re_path(r'api/kinopark/film/(?P<pk>[0-9]+)', views.movie_by_id),
    re_path(r'api/kinopark/films/unpublished', views.unpublished_movies),
    re_path(r'api/kinopark/register', views.sign_up)
]