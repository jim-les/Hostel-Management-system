from django.shortcuts import render
from Tenants.models import *

def home(request):
    return render(request, 'base.html')

def student(request):
    students = Student.objects.all()
    context = {
        "Students": students,
    }
    return render(request, 'Students.html', context)
