from django.db import models


# Custom User Model
class user(models.Model):
    firstname=models.CharField(max_length=255)
    lastname=models.CharField(max_length=255)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=12)
    password=models.CharField(max_length=20)
    role=models.CharField(max_length=20)

class DiagnosticTest(models.Model):
    patid = models.CharField(max_length=255)
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

