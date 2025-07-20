from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class Role(models.TextChoices):
    GUEST = 'guest', 'Guest'
    HOST = 'host', 'Host'
    ADMIN = 'admin', 'Admin'


class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.GUEST)
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.email} ({self.role})"
    

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4)
    sender_id = models.ForeignKey(User, models.CASCADE, related_name='sent_messages')
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4)
    participants_id = models.ForeignKey(User, models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)