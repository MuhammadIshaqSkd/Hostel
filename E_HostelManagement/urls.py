"""E_HostelManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from E_HostelManagement import settings
from Hostel_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('HostelCard/', views.HostelCard, name='HostelCard Page'),
    path('Hostel_details/<int:id>/', views.Hostel_details, name='Hostel_details Page'),
    path('Hostel_profile_img/', views.Hostel_profile_img, name='Hostel_profile_img update function'),
    path('booking_cancel_confirm/', views.booking_cancel_confirm, name='booking_cancel_confirm function'),

    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('hostelregistration', views.hostelregistration, name='hostelregistration'),
    path('seatbooking/', views.seatbooking, name='seatbooking'),
    path('complainreport/', views.complainreport, name='complainreport'),
    path('hosteldashboard/', views.hosteldashboard, name='hosteldashboard'),
    # path('hostelinfopage/', views.hostelinfopage, name='hostelinfopage'),
    path('maindashboard/', views.maindashboard, name='maindashboard'),
    path('test/', views.test, name='test'),
    path('viewallhostels/', views.viewallhostels, name='viewallhostels'),
    path('paymentgateway/', views.paymentgateway, name='paymentgateway'),
    # path('hostelportal/', views.hostelportal, name='hostelportal'),
    path('userportal/', views.userportal, name='userportal'),
    path('dashboard_profile/', views.dashboard_profile, name='dashboard_profile'),
    path("Login/", views.Login, name="Login"),
    path("register/", views.register, name="register"),
    path("seatconfirmation/", views.seatconfirmation, name="seatconfirmation"),
    # path("hostelportal/", views.hostelportal, name="hostelportal"),
    path("Logout/", views.Logout, name="Logout"),
    path("updateHostel_profile/", views.updateHostel_profile),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

