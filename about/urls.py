from django.urls import path
from . import views

urlpatterns = [
    path("", views.about_index, name="about_index"),
    path("<int:pk>/", views.about_detail, name="about_detail"),
    path("<category>/", views.about_category, name="about_category"),
]