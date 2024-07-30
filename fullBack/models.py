from django.db import models

class Agent(models.Model):
    id  = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=500)
    email =  models.CharField(max_length=100)
    type = models.CharField(max_length=30)
    password = models.CharField(max_length=16)

