from django.urls import path
from . import views

urlpatterns = [
    path('doctor/dashboard', views.doctordash,name='doctordash'),
    path('doctor/sheduler', views.shedulerdoctor,name='shedulerdoctor'),
    path('doctor/viewshedules', views.view_shedules,name='view_shedules'),
    path('doctor/add_presicription/<int:id>/<int:pid>', views.add_presicription,name='add_presicription')




]