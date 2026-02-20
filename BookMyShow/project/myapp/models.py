from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    def __str__(self):
        return self.username
    

class Movie(models.Model):
        title = models.CharField(max_length=100)
        description = models.TextField()
        release_date = models.DateField()
        image = models.ImageField(upload_to='movies/',null=True, blank=True)

        def __str__(self):
            return self.title
