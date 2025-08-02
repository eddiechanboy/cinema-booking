from django.contrib import admin

from .models import Movie, Cinema, Screen, Screening, Seat, Booking

admin.site.register([Movie, Cinema, Screen, Screening, Seat, Booking])
