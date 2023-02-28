from django.urls import path
# this imports all the views from the views.py
from . import views

urlpatterns = [
    # this is the home url
    path('', views.home, name='home'),
    # this is the single video url
    path('video-detail/<str:id>/', views.video_detail, name='video-detail'),
    # this is the add video url
    path('add-video/', views.add_video, name='add-video'),
    # this is the edit video url
    path('edit-video/<str:id>/', views.edit_video, name='edit-video'),
    # this is the delete video url
    path('delete-video/<str:id>/', views.delete_video, name='delete-video'),
    # this is the play video url
    path('play-video/<str:id>/<str:langid>/', views.play_video, name='play-video'),

] 
