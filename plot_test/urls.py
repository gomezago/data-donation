from django.urls import path
from . import views
from . import plot_example, plot2_example # Needs to be imported for some reason
urlpatterns = [
    path('plot/', views.plot_test, name='plot_test'),
    path('plot2/', views.plot_test_2, name='plot_2'),
]