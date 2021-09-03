from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.bucket_hello, name="hello"),
    path("new_project/", views.bucket_new, name="new"),
    path("project/", views.project_list, name="project_list"),
    path("project/<str:pk>/", views.project_view, name="project_view"),
    path("donation/<str:pk>/", views.donation_view, name="donation_view"),
    path("data_count/", views.get_data_count, name="data_count"),
    path("donation_count/", views.get_donations_count, name="donation_count"),
    path("data_time/<str:pk>", views.get_data, name="data_time"),
]