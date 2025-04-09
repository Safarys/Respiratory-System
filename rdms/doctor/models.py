from django.db import models
from predict.models import user
# Create your models here.

class Doctor(models.Model):
    userid = models.ForeignKey(user, on_delete=models.CASCADE)
    Specialization = models.CharField(max_length=40)
    medical_li_no = models.CharField(max_length=40)
    qualification = models.CharField(max_length=40)

class Sheduler(models.Model):
    userid = models.ForeignKey(user, on_delete=models.CASCADE)
    date_she = models.DateField()
    time_from = models.TimeField()
    time_to = models.TimeField()
    no_tokens = models.IntegerField()


class Prescription(models.Model):
    shedule_id = models.ForeignKey(Sheduler, on_delete=models.CASCADE)
    userid = models.ForeignKey(user, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    morning = models.BooleanField(default=False)
    afternoon = models.BooleanField(default=False)
    evening = models.BooleanField(default=False)
    duration = models.CharField(max_length=100)
    doctor_id=models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.medicine_name} for {self.userid}"    
    

class Patient(models.Model):
    userid=models.ForeignKey(user, on_delete=models.CASCADE)
    dob=models.DateField()
    gender=models.CharField(max_length=10)
    address=models.TextField(max_length=100)  


class Leave_doctor(models.Model):
    userid = models.ForeignKey(user, on_delete=models.CASCADE)
    date=models.DateField()
    reason=models.TextField()
    status=models.IntegerField()