from django.urls import path
from . import views

urlpatterns = [
    path('', views.pages_index, name='pages_index'),
    path("about/", views.pages_about, name="pages_about"),
]