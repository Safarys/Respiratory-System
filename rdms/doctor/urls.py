from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('doctor/dashboard', views.doctordash,name='doctordash'),
    path('doctor/sheduler', views.shedulerdoctor,name='shedulerdoctor'),
    path('doctor/viewshedules', views.view_shedules,name='view_shedules'),
    path('doctor/add_presicription/<int:id>/<int:pid>/', views.add_presicription, name='add_presicription'),
    path('doctor/patient_view_page/<int:id>/', views.patient_view_page,name='patient_view_page'),
    path('doctor/prescription/<int:userid>/', views.prescription_doctor_view, name='prescription_doctor_view'),
    path('doctor/logout_view', views.logout_view,name='logout_view'),
    path('doctor_appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('doctor/leave', views.leave, name='leave'),
    path('leave-status/', views.leave_status, name='leave_status'),




]