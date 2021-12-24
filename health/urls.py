from django.urls import path
from .import views

app_name = 'health'

urlpatterns = [
    path('home/', views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('audvid/', views.audvid, name="audvid"),
    path('audio/', views.audio, name="audio"),
    path('video/', views.video, name="video"),

]
