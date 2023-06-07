from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.bucket_hello, name="hello"),
    path("hello_first/", views.bucket_hello, name="first_hello"),
    path("new_project/", views.bucket_new, name="new"),
    path("project/", views.project_list, name="project_list"),
    path("project/<str:pk>/", views.project_view, name="project_view"),
    path("donation/<str:pk>/", views.donation_view, name="donation_view"),
    path("data_count/", views.get_data_count, name="data_count"),
    path("data_time/<str:pk>/", views.get_data, name="data_time"),
    path("metadata/<str:pk>/", views.metadata_view, name="metadata"),
    path("survey/<str:pk>/", views.survey_view, name="survey"),
    path("delete_survey/", views.delete_survey_view, name="delete_survey"),
    path('explore_data/<str:pk>/', views.explore_activity, name='exploration'),
    path('curate_data/<str:pk>/', views.curate, name='curation'),
    path('data_thanks/<str:pk>/', views.delete_thanks, name='deletion'),
]