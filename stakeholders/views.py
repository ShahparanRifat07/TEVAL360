from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Institution,Student,Parent,Department,Teacher
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from .resources import StudentResource
from tablib import Dataset
from django.urls import reverse
import traceback
# Create your views here.


def register(request):
    if request.method == "POST":
        institution_name = request.POST.get("institution_name")
        institution_code = request.POST.get("institution_code")
        established_year = request.POST.get("established_year")
        institution_type = request.POST.get("institution_type")
        institution_head = request.POST.get("institution_head")
        location = request.POST.get("location")
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        institution = Institution(institution_name=institution_name, institution_code=institution_code,
                                  established_year=established_year, institution_type=institution_type, institution_head=institution_head,
                                  location=location)

        institution._full_name = fullname
        institution._email = email
        institution._username = username
        institution._password = password

        institution.save()

        return redirect("stakeholder:login")
    elif request.method == "GET":
        return render(request, "register.html")
    


def admin_dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        institution = Institution.objects.filter(institution_admin=user)
        if institution:
            context={
                'admin' : institution[0].institution_admin,
            }
            return render(request,'admin_dashboard.html',context)
        else:
            return HttpResponse("you are not an admin")
    else:
        return redirect('stakeholder:login')
    

def student_dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        student = Student.objects.get(user= user)
        if student is not None:
            context = {
                'student' : student,
            }
            return render(request,'student_dashboard.html',context)
        else:
            return HttpResponse("You are not a student")
    else:
        return redirect('stakeholder:login')
    

def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        institution = Institution.objects.filter(institution_admin=user)
        if institution:
            return redirect("stakeholder:admin-dashboard")
        else:
            student = Student.objects.get(user= user)
            if student is not None:
                return redirect("stakeholder:student-dashboard")
            else:
                pass
    else:
        return redirect('stakeholder:login')
    

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        
        try:
            user = authenticate(username= username,password = password)
            if user is not None:
                login(request,user)
                return dashboard(request)
            else:
                print("no user found---method=>user_login")
                return redirect("stakeholder:login")
        except:
            print("user does not exits==user_login")
            return redirect("stakeholder:login")
    elif request.method == "GET":
        return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('stakeholder:login')

