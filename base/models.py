from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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




    def __str__(self):
        return self.body[:50]


