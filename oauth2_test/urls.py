from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('login/', views.login, name='login'),
    path('autho/', views.auth, name='autho'),
    path('logout/', views.logout, name='logout'),
]