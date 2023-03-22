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
