import datetime
import os
import csv
import shutil
from django.http import JsonResponse
from django.shortcuts import redirect, render
from Tenants.models import Student, RentPayment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseServerError
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

@login_required
def home(request):
    students_count = Student.objects.count()
    students = Student.objects.all()
    current_month_amount = 0
    student_meals = Student.objects.filter(has_food = True).count()
    
    for student in students:
        current_month_amount += student.rent_amount
    
    context = {
        "Students": students_count,
        "current_month_amount": current_month_amount,
        "student_meals": student_meals,
    }
    return render(request, 'dashboard.html', context)

@login_required
def student(request):
    students = Student.objects.all()
    student_count = Student.objects.count()
    print(f"Number of students: {student_count}")
    context = {
        "Students": students,
    }
    return render(request, 'Students.html', context)

@login_required
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
            number = phone,
            has_food=bool(has_food),
        )
        
         # Add a success message
        messages.success(request, 'Student added successfully!')

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
        number = request.POST.get('phone')
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
        student.number = number
        student.has_food = bool(has_food)
        
        print(f"Phone number {student.number}")
        
        student.save()
        messages.success(request, 'Student updated successfully!')
        
        return redirect('student')

    # Redirect to student list page after successful update
    context = {
        "student": student,
    }
    return render(request, 'edit_student.html', context)
    

def delete_student(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        user = student.user
        student.delete()
        user.delete()
        messages.success(request, 'Student deleted successfully!')
        
        return redirect('student')

    except Student.DoesNotExist:
        return JsonResponse({"error": "Student not found"}, status=404)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

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


def update_arrears(request):
    students = Student.objects.all()
    for student in students:
        student.update_all_arrears()  # Call the method on each student instance
    messages.success(request, 'Arrears updated successfully!')
    return redirect('student')

def transaction(request):
    students = Student.objects.all()
    rentpayment = RentPayment.objects.all().order_by('-date_paid')  
    context = {
        "Students": students,
        "RentPayment": rentpayment
    }
    return render(request, 'transaction/transaction.html', context)


def add_rentpayment(request):
    students = Student.objects.all()
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        amount = request.POST.get('amount')
        month = request.POST.get('month')
        date = request.POST.get('date')
        mpesa_ref = request.POST.get('mpesa_ref')
        reciept = request.POST.get('reciept')
        
        student = Student.objects.get(id=full_name)
        # check if renpayment with mpesa_ref already exists
        
        if RentPayment.objects.filter(mpesa_ref=mpesa_ref).exists():
            message = f'Rent payment with that mpesa ref ({mpesa_ref}) already exists'
            messages.error(request, message)
            return redirect('transaction')
        
        RentPayment.objects.create(
            student=student,
            amount=amount,
            month_paid=month,
            date_paid=date,
            mpesa_ref=mpesa_ref,
            reciept=reciept
        )

        message = 'Rent payment added successfully'
        messages.success(request, message)
        
    else:
        message ='Invalid request method'
        messages.success(request, message)
    
    rentpayment = RentPayment.objects.all().order_by('-date_paid')  
    context = {
        "Students": students,
        "RentPayment": rentpayment
    }
    return render(request, 'transaction/transaction.html', context)
    


def get_student_rent_payments(request):
    student_id = request.GET.get('student_id')
    rent_payments = RentPayment.objects.filter(student_id=student_id).order_by('date_paid')
    payments_data = []
    for payment in rent_payments:
        payments_data.append({
            'amount': float(payment.amount),
            'month_paid': payment.month_paid,
            'reciept': payment.reciept,
            'mpesa_ref': payment.mpesa_ref,
            'date_paid': payment.date_paid.strftime('%Y-%m-%d'),
            'balance': float(payment.student.arrears)
        })
    return JsonResponse(payments_data, safe=False)

def delete_rent_payment(request, payment_id):
    payment = RentPayment.objects.get(id=payment_id)
    student = payment.student
    payment.delete()
    return redirect('transaction')


def underContruction(request):
    return render(request, 'underConstruction.html')


# define util functions
def get_dashboard_data(request):
    try:
        month = request.GET.get('month', None)
        print(f"Month Range: {month}")
        # get the current month with python
        students_count = Student.objects.count()
        transactions = RentPayment.objects.filter(month_paid=month)
        students = Student.objects.all()
        total_payment = sum(student.rent_amount for student in students)
        print(total_payment)
        current_month_amount = sum(transaction.amount for transaction in transactions)
        arrears = sum(student.arrears for student in students)
        student_meals = Student.objects.filter(has_food = True).count()
        
        context = {
            "Students": students_count,  # Adjust based on your model
            "current_month_amount": current_month_amount,
            "arrears": abs(arrears),
            "student_meals": student_meals,
            "total_payment": total_payment
        }
        return JsonResponse(context, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
import datetime
def export_students_csv(request):
    # Define the response with the appropriate content type for CSV
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="students-{date}.csv"'

    # Create a CSV writer object
    writer = csv.writer(response)

    # Define the CSV header
    writer.writerow(['Username', 'Full Name', 'Room Number', 'Rent Amount', 'Arrears', 'Has Food', 'Admission Date', 'Contact Number'])

    # Write student data rows
    for student in Student.objects.all():
        writer.writerow([
            student.user.username,
            f"{student.user.first_name} {student.user.last_name}",
            student.room_number,
            student.rent_amount,
            student.arrears,
            'Yes' if student.has_food else 'No',
            student.adm_date,
            student.number
        ])

    return response
    
def statistics(request):
    students = Student.objects.all()
    total_students = students.count()
    total_rent = sum(student.rent_amount for student in students)
    total_arrears = sum(student.arrears for student in students)
    total_meals = Student.objects.filter(has_food=True).count()
    context = {
        'total_students': total_students,
        'total_rent': total_rent,
        'total_arrears': total_arrears,
        'total_meals': total_meals
    }
    return render(request, 'statistics/statistics.html', context)

def print_transactions(requests):
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    month = requests.POST.get('month')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="transactions-{date}.csv"'

    if month:
        if month == "all":
            transactions = RentPayment.objects.all()
        
        else:
            transactions = RentPayment.objects.filter(month_paid=month)
    else:
        return HttpResponse("Invalid request")
    
    writer = csv.writer(response)
    writer.writerow(['Full Name', 'Amount', 'Month Paid', 'Mpesa Ref', 'Date Paid', 'Reciept'])
    for transaction in transactions:
        writer.writerow([
            transaction.student.user.first_name + " " + transaction.student.user.last_name,
            transaction.amount,
            transaction.month_paid,
            transaction.mpesa_ref,
            transaction.date_paid,
            transaction.reciept
        ])
    return response

@login_required
def backupPage(request):
    # Define the path to the SQLite database file
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    backup_dir = os.path.join(settings.BASE_DIR, 'backup')

    # Ensure the backup directory exists
    os.makedirs(backup_dir, exist_ok=True)

    # Fetch the last backup file details
    backup_files = [f for f in os.listdir(backup_dir) if os.path.isfile(os.path.join(backup_dir, f))]
    backup_files.sort(key=lambda f: os.path.getmtime(os.path.join(backup_dir, f)), reverse=True)
    
    if backup_files:
        last_backup_file = backup_files[0]
        last_backup_path = os.path.join(backup_dir, last_backup_file)
        last_backup_time = datetime.fromtimestamp(os.path.getmtime(last_backup_path)).strftime('%Y-%m-%d %H:%M:%S')
        last_backup_size = os.path.getsize(last_backup_path) / 1024  # size in KB
    else:
        last_backup_file = None
        last_backup_time = None
        last_backup_size = None

    context = {
        'last_backup_file': last_backup_file,
        'last_backup_time': last_backup_time,
        'last_backup_size': f"{last_backup_size:.2f} KB" if last_backup_size else None,
    }

    return render(request, 'backup.html', context)

@login_required
def backup_database(request):
    try:
        # Define the path to the SQLite database file
        db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')

        # Check if the database file exists
        if not os.path.exists(db_path):
            return HttpResponseServerError("Database file does not exist.")

        # Define the backup file path
        backup_path = os.path.join(settings.BASE_DIR, 'backup', 'db_backup.sqlite3')

        # Ensure the backup directory exists
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)

        # Copy the database file to the backup path
        shutil.copy2(db_path, backup_path)

        # Read the file content to return as a response
        with open(backup_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/x-sqlite3')
            response['Content-Disposition'] = f'attachment; filename="db_backup.sqlite3"'

        # Optionally delete the backup file after sending it
        os.remove(backup_path)

        return response
    except Exception as e:
        return HttpResponseServerError(f"An error occurred during backup: {str(e)}")
    

def restore_database(request):
    if request.method == 'POST':
        backup_file = request.FILES['backup_file']
        backup_path = default_storage.save('backup_file.sqlite3', ContentFile(backup_file.read()))
        new_db_path = default_storage.path(backup_path)
        current_db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')

        # Ensure the current database is safely replaced
        try:
            # Backup current database before replacing
            current_db_backup_path = os.path.join(settings.BASE_DIR, 'db_backup_current.sqlite3')
            shutil.copy2(current_db_path, current_db_backup_path)

            # Replace the current database with the uploaded one
            os.replace(new_db_path, current_db_path)

            messages.success(request, 'Database restored successfully. Please restart the server.')
        except Exception as e:
            messages.error(request, f"An error occurred during restoration: {str(e)}")
            return redirect('backupPage')

        return redirect('backupPage')
    else:
        messages.error(request, "Invalid request method for restoration.")
        return redirect('backupPage')