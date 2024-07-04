from django.urls import path
from django.urls import include, path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('student/', student, name='student'),
    path('add_student/', add_student, name='add_student'),
    path('edit_student/<int:student_id>/', edit_student, name='edit_student'),
    path('delete_student/<int:student_id>/', delete_student, name='delete_student'),
    path('student_details/', get_student_details, name='get_student_details'),
    path('search_student/', search_student, name='search_student'),
    path('update_arrears/', update_arrears, name='update_arrears'),
    path('students/rent_payments/', get_student_rent_payments, name='get_student_rent_payments'),
    path('delete_rent_payment/<int:payment_id>/', delete_rent_payment, name='delete_rent_payment'),
    path('transaction/', transaction, name='transaction'),
    path('add_rentpayment/', add_rentpayment, name='add_rentpayment'),
    path('underConstruction', underContruction, name='underContruction'),
    path('get_dashboard_data/', get_dashboard_data, name='get_dashboard_data'),
    path('export-students-csv/', export_students_csv, name='export_students_csv'),
    path('statistics/', statistics, name='statistics'),
    path('print_transactions/', print_transactions, name='print_transactions'),
    path('backuppage/', backupPage, name='backupPage'),
    path('backup/', backup_database, name='backup_database'),
    path('restore/', restore_database, name='restore_database'),
]
    