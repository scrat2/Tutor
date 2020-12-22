"""
URLs list for lesson app. Put different links here and they will be add in /Tutor/urls.py.
"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.connexion),
    path('profil/', views.profil),
    path('home/', views.home),
    path('add/', views.add),
    path('search/', views.search),
]
