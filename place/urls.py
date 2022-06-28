from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginpage, name="login"),
    path('logout/', views.logoutpage, name="logout"),
    path('register/', views.registerpage, name="register"),
    path('places/<str:pk>/', views.place, name="places"),
    path('create-place/', views.createplace, name="create-place"),
    path('update-place/<str:pk>/', views.updateplace, name="update-place"),
    path('delete-place/<str:pk>/', views.deleteplace, name="delete-place"),
    path('delete-comment/<str:pk>/', views.deletecomment, name="delete-comment"),
    path('user-profile/<str:pk>/', views.userprofile, name="user-profile"),
    path('update-user/', views.updateuser, name="update-user"),
    path('mobile-topic/', views.topicpage, name="mobile-topics"),
    path('mobile-activity/', views.activitypage, name="mobile-activity")
]
