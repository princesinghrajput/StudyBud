from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio=models.TextField(null=True)

    #avatar

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS = []

class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

 


class Room(models.Model):
    #host
    host=models.ForeignKey(User, on_delete=models.SET_NULL, null=True )
    name = models.CharField(max_length=100)
    #topic
    topic=models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    participants=models.ManyToManyField(User, related_name='participants', blank=True)
    description = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at', 'updated_at']


class Message(models.Model):
    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    body=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    

    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.body[:50]
       


