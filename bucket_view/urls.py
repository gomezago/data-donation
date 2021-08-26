from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.bucket_hello, name="hello"),
    path("new_project/", views.bucket_new, name="new"),
    path("project/", views.project_list, name="project_list"),
    path("project/<str:pk>/", views.project_view, name="project_view"),
]