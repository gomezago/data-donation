from django.urls import path
from . import views

urlpatterns = [
    path("", views.cause_index, name="cause_index"),
    path("<int:pk>/", views.cause_detail, name="cause_detail"), # Dynamically generate URLs
]