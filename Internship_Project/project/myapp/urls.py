from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('show/<int:show_id>/', views.show_detail, name='show_detail'),
    path('mybookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('add-movie/', views.add_movie, name='add_movie'),
    
]