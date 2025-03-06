from django.conf import settings
from django.urls import path,include
from . import views

urlpatterns = [
    path('login/', views.login,name='login'),
    path('register/',views.register,name='register'),
    path('',views.home,name='home'),


]