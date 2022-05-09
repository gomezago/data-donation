from django.urls import path
from . import views
from . import point_selection, point_exploration, receiver_exploration # Needs to be imported for some reason
urlpatterns = [
    path('select/<str:pk>/', views.select_point, name='select'),
    path('explore/<str:pk>/', views.explore_point, name='explore'),
    path('overview/<str:pk>/', views.receiver_view, name='receive'),
    path('overview_user/<str:pk>/', views.receiver_explore, name='receive_explore'),
]