from urllib import request

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Booking, Show
from django.contrib import messages
from.models import Movie
from django.contrib.auth.decorators import login_required
from .models import Booking,Seat
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages
# Create your views here.

def home(request):
    movies=Movie.objects.all()
    return render(request, "myapp/home.html", {"movies": movies})

@login_required(login_url="login")
def show_detail(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    available_seats = Seat.objects.filter(show=show, is_booked=False).count()

    if request.method == "POST":

        # checkbox se selected seats lena
        selected_seats = request.POST.getlist("selected_seats")

        seats_requested = len(selected_seats)

        available_seats = Seat.objects.filter(show=show, is_booked=False).count()

        if seats_requested > 0 and seats_requested <= available_seats:

            total_amount = seats_requested * show.price

            booking = Booking.objects.create(
                user=request.user,
                show=show,
            )

            seats = Seat.objects.filter(id__in=selected_seats, is_booked=False)

            for seat in seats:
                seat.is_booked = True
                seat.save()
                booking.seats.add(seat)

            messages.success(
                request,
                f"Booked {seats_requested} Seats successfully! Total amount: ₹{total_amount}"
            )

            return redirect("home")

        else:
            messages.error(request, "Please select valid seats.")

    seats = Seat.objects.filter(show=show)

    return render(request, "myapp/show_detail.html", {
        "show": show,
        "available_seats": available_seats,
        "seats": seats
    })



@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-id')

    for booking in bookings:
        # booking.total_amount = booking.seats_booked * booking.show.price
        booking.total_amount = booking.seats.count() * booking.show.price
    return render(request, "myapp/my_bookings.html", {"bookings": bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    # seats add back
    show = booking.show

    # show.available_seats += booking.seats_booked
    # show.save()
    for seat in booking.seats.all():
        seat.is_booked = False
        seat.save()


    # booking record delete
    booking.delete()
    messages.success(request, "Booking cancelled successfully.")
    return redirect("my_bookings")



def admin_check(user):
    if not user.is_staff:
        raise PermissionDenied
    return True
@login_required
@user_passes_test(admin_check)

def add_movie(request):
   return render(request, "myapp/add_movie.html")







def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect("login")
    else:
        form = CustomUserCreationForm()

    return render(request, "myapp/signup.html", {"form": form})


   