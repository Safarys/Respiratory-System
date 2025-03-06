from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('patients/', views.patient_dashboard,name='patients_dash'),
    

]