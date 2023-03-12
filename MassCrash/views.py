from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import User


@csrf_exempt
def user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        location = request.POST.get('location')
        user = User(email=email, location=location)
        user.save()
        return render(request, 'success.html')
    return render(request, 'index.html')
