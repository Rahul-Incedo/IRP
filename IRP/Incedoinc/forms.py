from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Employee



class SignUpForm(UserCreationForm):
    
    first_name = forms.CharField(max_length=64, required=True)
    last_name = forms.CharField(max_length=64, required=False)
    email = forms.EmailField(max_length=254, required = 'True')
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1','password2']

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


class LoginForm(AuthenticationForm):
    email = forms.EmailField(max_length=254, required = 'True')
    class Meta:
        model = User
        fields = ['username', 'email', 'password']   

 

    