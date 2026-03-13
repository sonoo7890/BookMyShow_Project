# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Show, Seat

# @receiver(post_save, sender=Show)
# def create_seats_for_show(sender, instance, created, **kwargs):
#     if created:
#         rows = ['A', 'B', 'C']
#         seats_per_row = 10

#         for row in rows:
#             for num in range(1, seats_per_row + 1):
#                 Seat.objects.create(
#                     show=instance,
#                     seat_number=f"{row}{num}"
#                 )

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Show, Seat

@receiver(post_save, sender=Show)
def create_seats_for_show(sender, instance, created, **kwargs):
    if created:
        total = instance.total_seats

        for i in range(1, total + 1):
            Seat.objects.create(
                show=instance,
                seat_number=f"S{i}"
            )