from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('', views.home, name="home"),
    path('st_name/<str:pk>/', views.rooms, name="rooms"),
    path('new_room/', views.newRoom, name="new_room"),
    path('edit_room/<str:pk>/', views.editRoom, name="edit_room"),
    path('delete_room/<str:pk>/', views.deleteRoom, name="delete_room"),
    path('delete_message/<str:pk>/', views.deleteMessage, name="delete_message"),
    path('user_profile/<str:pk>/', views.userProfile, name="user_profile"),
    path('update_profile/', views.updateProfile, name='update_profile'),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),



]
