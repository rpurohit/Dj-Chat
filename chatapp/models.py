#chatapp/models.py
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Message(models.Model):
    author = models.ForeignKey(User, 
                               related_name='author_messages', 
                               on_delete=models.CASCADE)
    content = models.TextField()
    roomname = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.author.username

    def previous_messages(self, roomname):

        return Message.objects.filter(roomname=roomname).order_by('-timestamp').all()
