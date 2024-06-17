from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2, default=4000.00)
    has_food = models.BooleanField(default=False)
    arrears = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    adm_date = models.DateField(null=True)
    number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} (Room {self.room_number})"

    def update_arrears(self):
        total_rent = self.rent_amount
        payments = self.rentpayment_set.all()
        total_paid = sum(payment.amount for payment in payments)
        self.arrears = total_rent - total_paid
        self.save()

class RentPayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    month_paid = models.CharField(max_length=100)
    mpesa_ref = models.CharField(max_length=15)
    date_paid = models.DateTimeField(auto_now_add=True)
    reciept = models.CharField(max_length=15, null=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.amount} on {self.date_paid.strftime('%Y-%m-%d')}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.student.update_arrears()

class MealTransactions(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_paid = models.DateTimeField(auto_now_add=True)
    
    def calculate_arrears(self, default_meal_amount=2000):
        if self.amount < default_meal_amount:
            return default_meal_amount - self.amount
        else:
            return 0

class MealRecord(models.Model):
    MEAL_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    meal = models.CharField(max_length=10, choices=MEAL_CHOICES)
    date = models.DateField(default=timezone.now)
    served = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.username} - {self.meal} on {self.date}"

    class Meta:
        unique_together = ('student', 'meal', 'date')
        
    def save(self, *args, **kwargs):
        if not self.served and not MealRecord.objects.filter(student=self.student, meal=self.meal, date=self.date).exists():
            self.served = True
            super().save(*args, **kwargs)

class Query(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    query_text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    response_text = models.TextField(null=True, blank=True)
    responded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.username} - {self.query_text[:20]}"

class Notification(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.username} - {self.message[:20]}"
