from django.urls import path
from . import views

urlpatterns = [
    path('dataslip', views.atm, name='atm'),
    path('dataslip_pg', views.dataslip, name='dataslip_intro'),
    path('atm_transport/', views.atm_transport, name='atm_transport'),
    path('atm_food/', views.atm_food, name='atm_food'),
    path('atm_pay/', views.atm_pay, name='atm_pay'),
    path('atm_phone/', views.atm_phone, name='atm_phone'),
    path('atm_body/', views.atm_body, name='atm_body'),
    path('atm_print/', views.atm_printing, name='atm_print'),
    path('atm_donate/', views.atm_donate, name='atm_donate'),
    path('receipt/', views.receipt, name='receipt'),
    path('dataslip_feedback/', views.feedback, name='dataslip_feedback'),
    path('feedback_view/', views.feedback_back, name='feedback_view'),

]