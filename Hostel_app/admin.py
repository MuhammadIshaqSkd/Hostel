from django.contrib import admin
from Hostel_app.views import viewallhostels
from .models import Customer, Room, Registeredhostels, Seat_Booking


class HostelView(admin.ModelAdmin):
    pass


class Seat_BookingView(admin.ModelAdmin):
    readonly_fields = ['Seat_apply_date']


# Register your models here.

admin.site.register(Seat_Booking, Seat_BookingView)
admin.site.register(Customer)
admin.site.register(Room)
admin.site.register(Registeredhostels)
