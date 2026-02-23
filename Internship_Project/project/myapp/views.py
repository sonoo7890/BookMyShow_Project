from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Booking, Show
from django.contrib import messages
from.models import Movie
from django.contrib.auth.decorators import login_required
from .models import Booking
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

def home(request):
    movies=Movie.objects.all()
    return render(request, "myapp/home.html", {"movies": movies})


def show_detail(request, show_id):
    show = get_object_or_404(Show, id=show_id)

    if request.method == "POST":
        seats_requested= int(request.POST.get("seats"))

        if seats_requested <= show.available_seats:
            total_amount = seats_requested * show.price
            show.available_seats -= seats_requested
            show.save()

            # booking record create
            Booking.objects.create(
                user=request.user, 
                show=show,
                seats_booked=seats_requested
                )
            messages.success(request,f"Booked {seats_requested} Seats booked successfully! Total amount: ₹{total_amount}")
            return redirect("home")
            return HttpResponse("Not enough seats available.")
        else:
          
            messages.error(request, "Not enough seats available.")
    return render(request, "myapp/show_detail.html", {"show": show})




@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-id')

    for booking in bookings:
        booking.total_amount = booking.seats_booked * booking.show.price
    return render(request, "myapp/my_bookings.html", {"bookings": bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    # seats add back
    show = booking.show
    show.available_seats += booking.seats_booked
    show.save()
    # booking record delete
    booking.delete()
    messages.success(request, "Booking cancelled successfully.")
    return redirect("my_bookings")

def admin_check(user):
    return user.is_staff
@login_required
@user_passes_test(admin_check)

def add_movie(request):
    return render(request, "myapp/add_movie.html")