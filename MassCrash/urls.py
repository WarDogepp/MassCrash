from django.contrib import admin
from django.urls import path
from .views import user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', user, name='user'),
]
