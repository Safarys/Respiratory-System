from django.db import models


# Custom User Model
class user(models.Model):
    firstname=models.CharField(max_length=255)
    lastname=models.CharField(max_length=255)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=12)
    dob=models.DateField()
    gender=models.CharField(max_length=10)
    address=models.CharField(max_length=255)
    password=models.CharField(max_length=20)
    role=models.CharField(max_length=20)

class DiagnosticTest(models.Model):
    name = models.CharField(max_length=255)
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Doctor(models.Model):
    specialization=models.CharField(max_length=255)

class Appointment(models.Model):
    Appointment_date=models.DateField()
    Appointment_time=models.TimeField()

class Presecription(models.Model):
    prescribed_medicines=models.CharField(max_length=255)
    notes=models.CharField(max_length=255)
    date_issued=models.DateField()

class doctor_availability(models.Model):
    available_date=models.DateField()
    time_from=models.TimeField()
    time_to=models.TimeField()
    max_appointments=models.IntegerField()
