# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'room_number', 'email', 'phone', 'adm_date', 'rent_amount', 'arrears', 'has_food', 'profile']
    
    # Additional fields not in the model
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    profile = forms.ImageField(required=False)
    adm_date = forms.DateField()  # Add this line for admission date

    def save(self, commit=True):
        user = super(StudentForm, self).save(commit=False)
        user.username = f"{self.cleaned_data['first_name'].lower()}.{self.cleaned_data['last_name'].lower()}"
        user.email = self.cleaned_data['email']
        user.save()
        
        student = super().save(commit=False)
        student.user = user

        if commit:
            student.save()
        return student
