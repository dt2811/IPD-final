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
    path('record_audio/',views.audio_record,name="audio_record"),
    path('record_video/',views.video_record,name="video_record"),
    #path('details/',views.getItemDetails,name="details"),
    path("detail/<str:obj_id>/<str:user_id>/",views.getItemDetails,name="detail"),
    path("like/<str:obj_id>/<str:user_id>/",views.like_Item,name="like"),
    path("search/<str:id>/",views.searchbar,name="search"),

]
