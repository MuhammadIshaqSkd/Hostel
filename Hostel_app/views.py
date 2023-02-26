from datetime import datetime
from optparse import Option
from django.contrib import messages


from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.hashers import check_password, make_password
from .Middleware.User_auth import user_login_check, User_middleware, HostelUser_middleware
from django.core.paginator import Paginator



# Create your views here.
def index(request):
    # if request.method == 'GET':
    #     return render(request, 'index.html')
    # else:
    #     Data = request.POST
    #     email = Data.get('email')
    #     password = Data.get('password')

    #     # # Validations
    #     customer = Customer.objects.filter(email=email, password=password)
    #     customer_active = Customer.objects.filter(email=email, password=password, is_Active=True)
    #     error_message = None
    # if customer:
    #     if not customer_active:
    #         error_message = email + " is Deactivated by the TakeCare Team"
    #         return render(request, 'index.html', {'error': error_message})
    #     for i in customer:
    #         request.session['Customer_id'] = i.id
    #         request.session['Customer_email'] = i.email
    #         return redirect(maindashboard)
    # else:
    #     error_message = "Email or Password Invalid......"
    # return render(request, 'index.html', {'error': error_message})

    return render(request, 'index.html')


def HostelCard(request):
    # books = hostelregistration.objects.filter(Available_rooms__gte=1).order_by("-id")
    Hostels = Registeredhostels.objects.all().order_by("-id")
    paginator = Paginator(Hostels, 8)  # Show 8 contacts per page.
    page_number = request.GET.get('page')
    Hostel = paginator.get_page(page_number)
    Data = {'Hostel': Hostel}
    return render(request, 'HostelCardPage.html', Data)


def Hostel_details(request, id):
    hostel_details = Registeredhostels.objects.filter(id=id)
    data = {'hostel_details': hostel_details}
    return render(request, "Hostel_details.html", data)


def about(request):
    return render(request, 'about.html')


def viewallhostels(request):
    host = Customer.objects.all()
    Context = {
        'host': host
    }
    print(Context)
    return render(request, 'viewallhostels.html', Context)


def test(request):
    return render(request, 'test.html')


def services(request):
    return render(request, 'services.html')


def hostelregistration(request):
    if request.method == "POST":
        name = request.POST.get('name')
        Email = request.POST.get('email')
        Address = request.POST.get('address')
        City = request.POST.get('city')
        Password = request.POST.get('password')
        new_host = Registeredhostels(name=name, email=Email,
                                     password=Password, address=Address,
                                     city=City)
        Hostel_Owner = Registeredhostels.objects.filter(email=Email)
        if Hostel_Owner:
            messages.error(request, "this E-mail is already Register")
            return redirect(hostelregistration)
        new_host.save()
        messages.error(request, " Your account is Register successfully")
        return redirect(index)
    return render(request, 'hostelregistration.html')


# ////////////////// Customer Login/Registration Pages/////////////////////////////////////
@user_login_check
def Login(request):
    if request.method == 'POST':
        Data = request.POST
        email = Data.get('email')
        password = Data.get('pass')

        # Validations
        User = Customer.objects.filter(email=email)
        Hostel_Owner = Registeredhostels.objects.filter(email=email, password=password)

        User_active = Customer.objects.filter(email=email, is_Active=True)
        seller_active = Registeredhostels.objects.filter(email=email, is_Active=True)

        if User:
            customer = Customer.objects.get(email=email)
            if not User_active:
                messages.error(request, email + " is Deactivated by the our Team")
                return redirect(Login)
            flag = check_password(password, customer.password)
            if flag:
                request.session['id'] = customer.id
                request.session['Buyer_email'] = customer.email
                return redirect(maindashboard)
            else:
                messages.error(request, "Email or Password Invalid......")
                return redirect(Login)
        elif Hostel_Owner:
            hostel_Owner = Registeredhostels.objects.get(email=email, password=password)
            if not seller_active:
                messages.error(request, email + " is Deactivated by the our Team")
                return redirect(Login)
            request.session['Hostel_id'] = hostel_Owner.id
            request.session['Hostel_email'] = hostel_Owner.email
            return redirect(hosteldashboard)
        else:
            messages.error(request, "Email or Password Invalid......")
            return redirect(Login)
    else:
        if request.session.get("required_path"):
            path = request.session.get("required_path")
            return render(request, 'login.html', {'path': path})
        else:
            return render(request, 'login.html')


@user_login_check
def register(request):
    if request.method == 'POST':
        Data = request.POST
        Username = Data.get('name')
        email = Data.get('email')
        password = Data.get('pass')
        C_password = Data.get('re_pass')

        # Validations
        customer = Customer(name=Username, email=email, password=password)
        # Seller = seller(name=Username, email=email, password=password)

        if len(Username) < 4:
            messages.info(request, "Username must be 4 char long or more")
            return redirect(register)
        elif len(password) < 8:
            messages.info(request, "Password must be minimum 8 char long or more")
            return redirect(register)
        elif password != C_password:
            messages.info(request, "Password and Comfort Password must be same")
            return redirect(register)
        elif customer.isExits():
            messages.info(request, "Email Already Exits ")
            return redirect(register)
        elif Registeredhostels.isExits():
            messages.info(request, "Email Already Exits ")
            return redirect(register)

        else:
            # Creating New Account
            customer.password = make_password(customer.password)
            customer.save()
            messages.info(request, "Your account is created successfully.Now Please Login")
            return redirect(Login)
    else:
        return render(request, 'registration.html')


def Logout(request):
    Hostel_email = request.session.get('Hostel_email')
    Buyer_email = request.session.get('Buyer_email')

    if Hostel_email:
        request.session['Hostel_id'] = None
        request.session['Hostel_email'] = None
        request.session['required_path'] = None
        return redirect(index)
    elif Buyer_email:
        request.session['id'] = None
        request.session['Buyer_email'] = None
        request.session['required_path'] = None
        return redirect(maindashboard)
    return redirect(index)


# /////////////////////// Customer Login/Registration Pages END//////////////////////////////

def seatbooking(request):
    # host = seatbooking.objects.all()
    # Context = {
    #     'host': host
    # }
    return render(request, 'seatbooking.html')


def complainreport(request):
    return render(request, 'complainreport.html')


@User_middleware
def maindashboard(request):
    data = {}
    return render(request, 'maindashboard.html', data)


def registeredhostels(request):
    return render(request, 'viewallhostels.html')


def test(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        totalroom = request.POST['totalroom']
        address = request.POST['address']
        city = request.POST['city']
        password = request.POST['password']
        menu = request.POST['menu']
        new_test = test(name=name, email=email, totalroom=totalroom, address=address, city=city, password=password,
                        menu=menu)
        new_test.save()
        return HttpResponse('test added successfully')
    elif request.method == 'GET':
        return render(request, 'test.html')
    else:
        HttpResponse("An Error Occured: test is not added")


def paymentgateway(request):
    return render(request, 'paymentgateway.html')


@HostelUser_middleware
def hosteldashboard(request):
    Data = {}
    if request.session.get('Hostel_email'):
        Hostel_email = request.session.get('Hostel_email')
        Hostel = Registeredhostels.objects.get(email=Hostel_email)
        Hld = request.session.get('Hostel_id')
        Hostel_id = Registeredhostels.objects.get(id=Hld)
        Booking = Seat_Booking.objects.filter(hostel=Hostel_id)
        Data = {"Hostel": Hostel, 'Booking': Booking}
    return render(request, 'hostelportal.html', Data)


@HostelUser_middleware
def dashboard_profile(request):
    Data = {}
    if request.session.get('Hostel_email'):
        Hostel_email = request.session.get('Hostel_email')
        Hostel = Registeredhostels.objects.get(email=Hostel_email)
        Data = {"Hostel": Hostel}
    return render(request, 'dashboard_profile.html', Data)


@HostelUser_middleware
def updateHostel_profile(request):
    Data = {}
    if request.session.get('Hostel_email'):
        Hostel_email = request.session.get('Hostel_email')
        Hostel = Registeredhostels.objects.get(email=Hostel_email)
        if request.method == 'POST':
            data = request.POST
            hostel_number = data.get('hostel_number')
            one_bed = request.POST.get('one_bed')
            Two_bed = request.POST.get('Two_bed')
            Three_bed = request.POST.get('Three_bed')
            Four_bed = request.POST.get('Four_bed')
            one_bed_seat = data.get('one_bed_seat')
            Two_bed_seat = data.get('Two_bed_seat')
            Three_bed_seat = data.get('Three_bed_seat')
            Four_bed_seat = data.get('Four_bed_seat')
            description = data.get('description')
            Total_room = (int(one_bed) + int(Two_bed) + int(Three_bed) + int(Four_bed))
            Hostel.One_bed_rooms = one_bed
            Hostel.Two_bed_rooms = Two_bed
            Hostel.Three_bed_rooms = Three_bed
            Hostel.Four_bed_rooms = Four_bed
            Hostel.Total_rooms = Total_room
            Hostel.Onebed_per_seat_price = one_bed_seat
            Hostel.Two_bed_per_seat_price = Two_bed_seat
            Hostel.Three_bed_per_seat_price = Three_bed_seat
            Hostel.Four_bed_per_seat_price = Four_bed_seat
            Hostel.Description = description
            Hostel.hostel_number = hostel_number
            Hostel.save()
            messages.error(request, "Hostel detail is Updated Successfully")
            return redirect(updateHostel_profile)
        Data = {"Hostel": Hostel}
    return render(request, 'dashboard_profile.html', Data)


@HostelUser_middleware
def Hostel_profile_img(request):
    Hld = request.session.get('Hostel_id')
    error_message = None
    success = None
    Hostel_img = Registeredhostels.objects.get(id=Hld)
    if request.method == 'POST':
        hostel_profile_img = request.FILES.get('image')
        Hostel_img.hostel_img = hostel_profile_img
        Hostel_img.save()
        messages.error(request, "Hostel Profile Image is Updated Successfully")
    return redirect(dashboard_profile)


@HostelUser_middleware
def booking_cancel_confirm(request):
    if request.method == 'POST':
        Data = request.POST
        name = Data.get('action')
        id = Data.get('id')
        if name == 'cancel':
            order_Cancel = Seat_Booking.objects.get(id=id)
            order_Cancel.booking_status = 'Cancelled'
            order_Cancel.save()
            # Medicine = Seat_Booking.objects.get(id=order_Cancel.Medicine.id)
            # Medicine.Total_Stock = Medicine.Total_Stock + int(Quantity)
            # Medicine.save()
            messages.error(request, "Hostel Seat Booking is Cancel Successfully")
        else:
            order_Confirm = Seat_Booking.objects.get(id=id)
            order_Confirm.booking_status = 'Conform'
            order_Confirm.save()
            messages.error(request, "Hostel Seat Booking is Confirm Successfully")

    return redirect(hosteldashboard)


def userportal(request):
    return render(request, 'userportal.html')
def seatconfirmation(request):
    return render(request, 'seatconfirmation.html')





