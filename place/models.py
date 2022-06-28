from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True, unique=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    bio = models.TextField(null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Places(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    upload_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    located = models.CharField(max_length=200)
    hotel_name = models.CharField(max_length=200)
    description = models.TextField()
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Places, on_delete=models.CASCADE)
    order_hotel = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_hotel
