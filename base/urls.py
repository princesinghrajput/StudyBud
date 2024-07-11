from django.urls import path
from . import views

urlpatterns = [
  
    path('',views.home, name='home' ),
    path('room/', views.room),

    path('room/<str:pk>/', views.room, name='room'),
   
    path('about/', views.about),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),



]
