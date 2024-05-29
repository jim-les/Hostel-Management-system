# rent/admin.py

from django.contrib import admin
from .models import Student, RentPayment, MealRecord, Query, Notification

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'room_number', 'has_food', 'arrears')
    search_fields = ('user__username', 'room_number')
    list_filter = ('has_food',)

class RentPaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'date_paid')
    search_fields = ('student__user__username',)
    list_filter = ('date_paid',)

class MealRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'meal', 'date', 'served')
    search_fields = ('student__user__username',)
    list_filter = ('meal', 'date', 'served')

class QueryAdmin(admin.ModelAdmin):
    list_display = ('student', 'query_text', 'date_posted', 'responded')
    search_fields = ('student__user__username', 'query_text')
    list_filter = ('responded', 'date_posted')

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('student', 'message', 'date_sent', 'read')
    search_fields = ('student__user__username', 'message')
    list_filter = ('read', 'date_sent')

admin.site.register(Student, StudentAdmin)
admin.site.register(RentPayment, RentPaymentAdmin)
admin.site.register(MealRecord, MealRecordAdmin)
admin.site.register(Query, QueryAdmin)
admin.site.register(Notification, NotificationAdmin)
