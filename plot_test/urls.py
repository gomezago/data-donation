from django.urls import path
from . import views
from . import point_selection # Needs to be imported for some reason
urlpatterns = [
    path('select/<str:pk>/', views.select_point, name='select'),
]