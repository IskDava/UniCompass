from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('fyp', views.show_fyp, name="for you page"),
    path('explore', views.show_search, name="explore"),
    path('uni/<int:id>', views.get_uni, name="uni info"),
    path('search', views.search, name="search")
]
