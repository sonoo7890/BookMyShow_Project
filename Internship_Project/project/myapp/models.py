from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'), 
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES,)


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField()
    release_date = models.DateField()
    image = models.ImageField(upload_to='movies/', null=True, blank=True)

    def __str__(self):
        return self.title


class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    show_time = models.DateTimeField()
    price = models.IntegerField( )
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()


class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seats_booked = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)

    