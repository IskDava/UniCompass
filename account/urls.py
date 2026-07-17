from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.test, name="test"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('verification', views.verification, name="verification"),
    path('activate', views.activate_account, name="activate account"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('delete', views.delete_account, name="delete account"),
    path('preferences/save', views.save_preferences, name="save preferences"),
    path('preferences/majors', views.show_majors, name="majors page"),
    path('preferences/select_majors', views.select_majors, name="select majors"),
    path('preferences/competencies', views.show_compet, name="competencies page"),
    path('preferences/select_compets', views.select_compets, name="select competencies"),
    path('preferences', views.show_preferences, name="show preferences"),
    path('profile', views.profile, name="profile"),
]
