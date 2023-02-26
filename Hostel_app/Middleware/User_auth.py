from django.contrib import messages
from django.shortcuts import redirect


def user_login_check(get_response):
    def middleware(request):

        if request.session.get('Hostel_email'):
            return redirect('/hosteldashboard/')
        elif request.session.get('Buyer_email'):
            return redirect('/maindashboard/')

        response = get_response(request)
        return response

    return middleware


def User_middleware(get_response):
    def middleware(request):
        if not request.session.get('Buyer_email'):
            messages.error(request, "Please Login First For Future Operations")
            request.session['required_path'] = request.path
            return redirect('/Login/?next=%s' % request.path)

        response = get_response(request)
        return response

    return middleware


def HostelUser_middleware(get_response):
    def middleware(request):
        if not request.session.get('Hostel_email'):
            messages.error(request, "Please Login First For Future Operations")
            request.session['required_path'] = request.path
            return redirect('/Login/?next=%s' % request.path)

        response = get_response(request)
        return response

    return middleware
