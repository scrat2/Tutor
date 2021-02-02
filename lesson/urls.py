"""
URLs list for lesson app. Put different links here and they will be add in /Tutor/urls.py.
"""
from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.connexion),
    path('profil/', views.profil),
    path('home/', views.home),
    # path('add/', views.add),
    path('search/', views.search),
    path('logout/', views.view_logout),
    path('load_search/', views.load_search),
    re_path(r'^subscribe/(?P<lesson_id>[0-9]+)/$', views.subscribe),
]
