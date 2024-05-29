from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Student, RentPayment, MealRecord, Query, Notification
# from .forms import MealRecordForm, QueryForm, RentPaymentForm

@login_required
def dashboard(request):
    student = Student.objects.get(user=request.user)
    rent_payments = RentPayment.objects.filter(student=student)
    meal_records = MealRecord.objects.filter(student=student)
    queries = Query.objects.filter(student=student)
    notifications = Notification.objects.filter(student=student)
    return render(request, 'index.html', {
        'student': student,
        'rent_payments': rent_payments,
        'meal_records': meal_records,
        'queries': queries,
        'notifications': notifications,
    })

# @login_required
# def respond_to_query(request, query_id):
#     query = get_object_or_404(Query, id=query_id)
#     if request.method == 'POST':
#         response_text = request.POST.get('response_text')
#         query.response_text = response_text
#         query.responded = True
#         query.save()
#         Notification.objects.create(student=query.student, message=f"Response to your query: {response_text}")
#         return redirect('dashboard')
#     return render(request, 'rent/respond_to_query.html', {'query': query})