from django.core import validators
from django import forms
from Incedoinc.models import Candidate, Job, TestModel, Employee

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    employee_id = forms.CharField(max_length=20, required=True)
    full_name = forms.CharField(max_length=64, required=True)
    email = forms.EmailField(max_length=254, required =True)
    password= forms.CharField(max_length=10)

    class Meta:
        model = Employee
        fields = ['full_name', 'email', 'employee_id', 'password']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        if "@incedoinc.com" not in email:
            raise forms.ValidationError("Must be an Incedo Email address")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username = username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
