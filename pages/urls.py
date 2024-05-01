from django.urls import path
from . import views

urlpatterns = [
    path('', views.pages_index, name='pages_index'),
    path("about/", views.pages_about, name="pages_about"),
    path("people/", views.pages_questions, name="pages_questions"),
    path("publications/", views.pages_publications, name="pages_publications"),
    path("privacy/", views.pages_privacy, name="pages_privacy"),
    path("terms/", views.pages_terms, name="pages_terms"),
    path("extensions/", views.pages_extensions, name="pages_extensions"),
    path("howto/<str:pk>/", views.pages_instructions, name="pages_instructions"),
    path("afri_map/", views.pages_map, name="afri_map"),
]