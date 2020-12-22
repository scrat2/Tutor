from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Lessons(models.Model):
    nom = models.CharField(max_length=20, null=False)
    date_debut = models.DateField(null=False)
    date_fin = models.DateField(null=False)
    sujet = models.CharField(max_length=100, null=False)
    classe = models.CharField(max_length=20, null=False)
    teacher = models.CharField(max_length=20, null=False)
