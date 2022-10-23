from django.db import models
from datetime import datetime

# Create your models here.

class Register(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    reserver = models.CharField(max_length=50)
    start_date = models.DateTimeField("start date")
    end_date = models.DateTimeField("end date")

    #def __str__(self):
        #return self.start_date

class ReservationJudge(models.Model):
    date = models.DateTimeField()
    state = models.IntegerField()

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")
