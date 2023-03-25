from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from geopy import distance
from .models import User


@csrf_exempt
def user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        location = request.POST.get('location')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        new_user = User(email=email, location=location, latitude=latitude, longitude=longitude)
        new_user.save()

        check_mass_crash(request)

        return render(request, 'success.html')
    return render(request, 'index.html')


def check_mass_crash(request):
    users = User.objects.filter(created_at__gte=timezone.now() - timezone.timedelta(seconds=10)).order_by(
        '-created_at')[:3]
    if len(users) == 3:
        user_locations = []
        for new_user in users:
            user_location = (new_user.latitude, new_user.longitude)
            user_locations.append(user_location)

        current_location = (request.POST.get('latitude'), request.POST.get('longitude'))
        mass_crash_radius = 10  # 10 метров

        for user_location in user_locations:
            if distance.distance(current_location, user_location).m <= mass_crash_radius:
                return render(request, 'mass_crash.html')

    return
