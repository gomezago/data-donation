from django.urls import path
from . import views
from . import plot_example # Needs to be imported for some reason
urlpatterns = [
    path('plot/', views.plot_test, name='plot_test')
]