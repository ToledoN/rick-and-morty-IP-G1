from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index-page'),
    path('login/', views.index_page, name='login'),
    path('home/', views.home, name='home'),

    path('favourites/', views.getAllFavouritesByUser, name='favoritos'),
    path('favourites/add/', views.saveFavourite, name='agregar-favorito'),
    path('favourites/delete/', views.deleteFavourite, name='borrar-favorito'),
    path('register/', views.register_view, name='register'),
    path('exit/', views.exit, name='exit'),
]