from django.urls import path
from . import views

urlpatterns = [
  
    path('',views.home, name='home' ),
    path('room/', views.room),

    path('room/<str:pk>/', views.room, name='room'),
   
    path('about/', views.about),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
    path('login/',views.loginPage, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('register/',views.registerPage, name='register'),
    path('delete-message/<str:pk>', views.deleteMessage, name='delete-message'),
    path('user-profile/<str:pk>', views.userProfile, name='user-profile'),
    path('update-profile/', views.updateProfile, name='update-profile'),
    path('user-setting/', views.userSetting, name='user-setting'),
    path('topics/', views.topicPage, name='topics'),
    path('activity/', views.activityPage, name='activity')

    



]
