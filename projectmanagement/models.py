from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class CustomUser(AbstractUser):
    mobile = models.BigIntegerField(null=True, blank=True)
    email = models.CharField(max_length=255)
    type_of_user = models.CharField(max_length=255)

    def __str__(self):
        return str(self.email)


class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, default=None)

    def __str__(self):
        return str(self.user)


class Project(models.Model):
    name = models.CharField(max_length=255)
    members = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    stage = models.CharField(max_length=255,default="")

    def __str__(self):
        return str(self.name) + "," + str(self.members)


class Task(models.Model):
    about = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True, default=None)
