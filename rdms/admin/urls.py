from django.urls import path
from . import views

urlpatterns = [
    path('Admin/admin_dashboard', views.admin_dashboard,name='admin_dashboard'),
  




]