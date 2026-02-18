from django.shortcuts import render

# Create your views here.
def landing(req):
    return render (req,'landing.html')
  
def  set(req):
    return render(req,'set.html')