from django.urls import re_path, path
from apps.kinopark import views
from .views import *
from .views import contact

urlpatterns = [
    re_path(r'api/kinopark/films$', views.movies_list),
    re_path(r'api/kinopark/film/(?P<pk>[0-9]+)', views.movie_by_id),
    re_path(r'api/kinopark/films/unpublished', views.unpublished_movies),
    # re_path(r'api/kinopark/register', views.sign_up)
    path('api/register', RegisterView.as_view()),
    path('api/login', LoginView.as_view()),
    path('api/user', UserView.as_view()),
    path('api/logout', LogoutView.as_view()),
    path('api/get_login', views.get_login),
    re_path(r'api/order/(?P<pk>[0-9]+)', views.get_order_by_id),
    re_path(r'api/kinopark/order', views.create_order),
    re_path(r'api/kinopark/seansy', views.seans_list),
    path('api/kinopark/seans/<int:id>', SeansView.as_view()),
    path('api/kinopark/ticket', TicketView.as_view()),
    path('api/kinopark/ticket/<int:id>', TicketView.as_view()),
    # re_path(r'api/kinopark/kinozal/(?P<id>[0-9]+)', views.kinozal_by_id),
    re_path(r'api/kinopark/seans/(?P<id>[0-9]+)', views.seans_by_id),
    path('api/kinopark/order/<int:id>', OrderView.as_view()),
    path('', views.contact)
]