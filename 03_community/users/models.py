from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    profile = models.ImageField(upload_to='profile/', default='profile/default.jpg', blank=True)
    bio = models.TextField(max_length=200, blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f" {self.username} - {self.email}"
 


