from .models import CustomUser
from django.core import validators
from django import forms


from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User




class SignUpForm(UserCreationForm):
    
    # name = forms.CharField(max_length=64, required=True)
    # email = forms.EmailField(max_length=254, required = 'True')
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password1','password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        if "@incedoinc.com" not in email:   
            raise forms.ValidationError("Must be an Incedo Email address")
        return email  
        
    





class LoginForm(AuthenticationForm):
    email = forms.EmailField(max_length=254, required = 'True')
    class Meta:
        model = CustomUser
        fields = ['email', 'password']   
