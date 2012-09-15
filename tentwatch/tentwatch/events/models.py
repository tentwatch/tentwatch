from django.db import models

# Create your models here.

class Event(models.Model):
    time = models.DateTimeField(auto_now_new=True)
    lat
