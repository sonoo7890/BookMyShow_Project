from django.shortcuts import render
from django.http import HttpResponse

from.models import Show
# Create your views here.

def home(request):
    shows=Show.objects.select_related('movie').all()
    return render(request, "myapp/home.html", {"shows": shows})
