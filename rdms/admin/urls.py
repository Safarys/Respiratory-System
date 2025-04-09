from django.urls import path
from . import views

urlpatterns = [
    path('Admin/admin_dashboard', views.admin_dashboard,name='admin_dashboard'),
  
 path('manage-leaves/', views.manage_leave_requests, name='manage_leave_requests'),
path('update-leave/<int:leave_id>/<str:action>/', views.update_leave_status, name='update_leave_status'),
 path('manage-doctors/', views.manage_doctors, name='manage_doctors'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),

 path('manage-patients/', views.manage_patients, name='manage_patients'),
    path('delete-patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),

]