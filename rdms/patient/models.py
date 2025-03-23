from django.db import models
from predict.models import user
from doctor.models import Sheduler
# Create your models here.

class Appointments(models.Model):
    shedule_id=models.ForeignKey(Sheduler, on_delete=models.CASCADE)
    userid=models.ForeignKey(user, on_delete=models.CASCADE)
