from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

# class LoginModel(models.Model):
#     name = models.CharField(max_length=30, blank=False)
#     mobile = models.CharField(max_length=10, null=False, blank=False, unique=True)
#     otp = models.CharField(max_length=5, blank=True)

# class CustomUser(AbstractUser):
    # name = models.CharField(max_length=30, blank=False)
    # mobile = models.CharField(max_length=10, null=False, blank=False, unique=True)
    # otp = models.CharField(max_length=5, blank=True)
    # pass

class LoginModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=5, blank=True, null=True)

class Results(models.Model):
    username = models.ForeignKey(LoginModel, on_delete=models.CASCADE)
    attempted_on =  models.DateTimeField(auto_now=True)
    result1 = models.CharField(max_length=100)