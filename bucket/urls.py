from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('login/', views.bucket_login, name='login'),
    path('auth/', views.auth, name='auth'),
    path('logout/', views.logout, name='logout'),
]