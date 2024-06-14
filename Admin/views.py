from django.http import JsonResponse
from django.shortcuts import redirect, render
from Tenants.models import *

def home(request):
    return render(request, 'base.html')

def student(request):
    students = Student.objects.all()
    context = {
        "Students": students,
    }
    return render(request, 'Students.html', context)


def add_student(request):
    if request.method == 'POST':
        # Extract data from POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        room_number = request.POST.get('room_number')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        adm_date = request.POST.get('adm_date')
        rent_amount = request.POST.get('rent_amount')
        arrears = request.POST.get('arrears')
        has_food = request.POST.get('has_food')

        # Create User object
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        # Create Student object
        student = Student.objects.create(
            user=user,
            room_number=room_number,
            rent_amount=rent_amount,
            arrears=arrears,
            adm_date=adm_date,
            has_food=bool(has_food),
        )

        # Redirect to student list page after successful creation
        return redirect('student')

    # If request method is not POST (e.g., GET), render the form page
    return render(request, 'Students.html')

def edit_student(request, student_id):
    student = Student.objects.get(id=student_id)
    if request.method == 'POST':
        # Extract data from POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        room_number = request.POST.get('room_number')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        adm_date = request.POST.get('adm_date')
        rent_amount = request.POST.get('rent_amount')
        arrears = request.POST.get('arrears')
        has_food = request.POST.get('has_food')

        # Update User object
        user = student.user
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Update Student object
        student.room_number = room_number
        student.rent_amount = rent_amount
        student.arrears = arrears
        student.adm_date = adm_date
        student.has_food = bool(has_food)
        student.save()
        return redirect('student')

    # Redirect to student list page after successful update
    context = {
        "student": student,
    }
    return render(request, 'edit_student.html', context)
    

def delete_student(request, student_id):
    student = Student.objects.get(id=student_id)
    student.delete()
    return redirect('student')

def get_student_details(request):
    student_id = request.GET.get('student_id')
    student = Student.objects.get(id=student_id)
    data = {
        'fullname': student.user.get_full_name(),
        'room_number': student.room_number,
        'rent_amount': student.rent_amount,
        'arrears': student.arrears,
        'has_food': student.has_food,
        'adm_date': student.adm_date.strftime('%Y-%m-%d') if student.adm_date else ''
    }
    return JsonResponse(data)

def search_student(request):
    query = request.GET.get('q', '')
    students = Student.objects.filter(user__username__icontains=query)
    context = {
        'Students': students
    }
    return render(request, 'components/student_list_items.html', context)

    