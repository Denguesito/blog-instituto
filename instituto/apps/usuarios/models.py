from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.email})"

