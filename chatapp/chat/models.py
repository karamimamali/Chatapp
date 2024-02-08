from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Message(models.Model):
    author = models.ForeignKey(User, related_name="author_messages" ,on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username
    
    def last_15_messages():
        return Message.objects.order_by("-timestamp").all()[:15]


class ChatGroup(models.Model):
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    