from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('patients/', views.patient_dashboard,name='patients_dash'),
    path('patients/patientappointment', views.patientappointment,name='patientappointment'),
    path('patients/patientappointment/Sleep', views.patientappointment_Sleep,name='patientappointment_Sleep'),
    path('patients/patientappointment/Pulmonologist', views.patientappointment_Pulmonologist,name='patientappointment_Pulmonologist'),
    path('patients/patientappointment/Allergist', views.patientappointment_Allergist,name='patientappointment_Allergist'),
    path('patientappointment/book_shedule/<int:id>/', views.book_shedule, name='book_shedule'),
    path('patientappointment/precription_new_page/<int:id>/', views.prescription_new_page, name='precription_new_page'),
    path('patientappointment/bookingshowpage', views.bookingshowpage, name='bookingshowpage'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),

    path('patientappointment/test_view', views.test_view, name='test_view'),

    path('my-appointments/', views.patient_appointments_view, name='patient_appointments'),



    

]