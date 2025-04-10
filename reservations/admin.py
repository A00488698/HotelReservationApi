from django.contrib import admin

# Register your models here.
from .models import Hotel, Reservation

admin.site.register(Hotel)
admin.site.register(Reservation)
