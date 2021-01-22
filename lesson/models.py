from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Lessons(models.Model):
    nom = models.CharField(max_length=20, null=False)
    date = models.DateField(null=False)
    begin = models.TimeField(null=False)
    end = models.TimeField(null=False)
    sujet = models.CharField(max_length=200, null=False)
    promo = models.CharField(max_length=20, null=False)
    campus = models.CharField(max_length=20, null=False)
    salle = models.CharField(max_length=20, null=False)


class Profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    campus = models.CharField(max_length=20, null=True)
    promo = models.CharField(max_length=20, null=True)
    nbr_heure = models.IntegerField(null=False, default=0)


class Groups(models.Model):
    lessonID = models.ForeignKey(Lessons, on_delete=models.CASCADE)
    profileID = models.ForeignKey(Profiles, on_delete=models.CASCADE)
    teacher = models.BooleanField(default=False)
