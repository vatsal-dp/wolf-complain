from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from .models import *

def is_logged(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_authenticated:
                group = Group.objects.get(user = request.user)
                if group.name == 'faculty':
                    if Admin(user=request.user).designation == 'Principal':
                        return redirect('principaldashboard')
                    else:
                        return redirect('admindashboard')
                else:
                    return redirect('studentdashboard')
            else:
                return view_func(request, *args, **kwargs)
        return wrapper_func



def student_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = Group.objects.get(user = request.user)
        if group.name == 'student':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to view this page.')
    return wrapper_func

# def student_required(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         group = Group.objects.get(user = request.user)
#         if group.name == 'student':
#             return view_func(request, *args, **kwargs)
#         else:
#             return HttpResponse('You are not authorized to view this page.')
#     return wrapper_func

def admin_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = Group.objects.get(user = request.user)
        if group.name == 'faculty':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to view this page.')
    return wrapper_func

def adminprofile_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        profile = Admin.objects.filter(user = request.user).count()
        if profile == 0:
            return redirect('adminProfile')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def studentprofile_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        profile = Student.objects.filter(user = request.user).count()
        if profile == 0:
            return redirect('studentProfile')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
