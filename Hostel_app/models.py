from django.utils import timezone
from django.db import models
from datetime import datetime


# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=200, default='')
    email = models.EmailField(default='')
    address = models.CharField(max_length=200, default='')
    password = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=200, default='')
    menu = models.CharField(max_length=200, default='')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    forget_password_token = models.CharField(max_length=100, null=True, blank=True)
    is_Active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def isExits(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False


class Registeredhostels(models.Model):
    name = models.CharField(max_length=100, null=True, default='')
    hostel_number = models.PositiveBigIntegerField(default=0)
    hostel_img = models.ImageField(upload_to="Hostel_img/", null=True, blank=True)
    email = models.EmailField(default='')
    password = models.CharField(max_length=100, default='')
    address = models.TextField(max_length=300, default="", null=True, blank=True)
    city = models.TextField(max_length=100, default='')
    Total_rooms = models.PositiveIntegerField(default=0)
    Available_rooms = models.PositiveIntegerField(default=0)
    One_bed_rooms = models.PositiveIntegerField(default=0)
    Onebed_per_seat_price = models.PositiveIntegerField(default=0)
    Two_bed_rooms = models.PositiveIntegerField(default=0)
    Two_bed_per_seat_price = models.PositiveIntegerField(default=0)
    Three_bed_rooms = models.PositiveIntegerField(default=0)
    Three_bed_per_seat_price = models.PositiveIntegerField(default=0)
    Four_bed_rooms = models.PositiveIntegerField(default=0)
    Four_bed_per_seat_price = models.PositiveIntegerField(default=0)
    Description = models.TextField(default='')
    is_Active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    def isExits(self):
        if Registeredhostels.objects.filter(email=self.email):
            return True
        return False


class Room(models.Model):
    Room_number = models.CharField(max_length=100)
    seat = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.Room_number


class Seat_Booking(models.Model):
    Seat = (
        ('one bed', 'one bed'),
        ('Two bed', 'Two bed'),
        ('Three bed', 'Three bed'),
        ('Four bed', 'Four bed'),
    )
    STATUS = (
        ('Pending', 'Pending'),
        ('Conform', 'Conform'),
        ('Cancelled', 'Cancelled'),
    )
    Seat_number = models.CharField(max_length=100, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, default=None)
    hostel = models.ForeignKey(Registeredhostels, on_delete=models.CASCADE, default=None)
    price = models.PositiveIntegerField(default=0)
    booking_status = models.CharField(max_length=50, choices=STATUS, default='Pending')
    seat_type = models.CharField(max_length=200, choices=Seat, null=True)
    Booked_date = models.DateField(default=timezone.now)
    Seat_apply_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer.name
