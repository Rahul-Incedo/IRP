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
        
        fields = ['employee_id', 'username','name', 'password1','password2']  #username is email
         

    def clean_employee_id(self):
       
        employee_id = self.cleaned_data['employee_id']
        if CustomUser.objects.filter(employee_id = employee_id).exists():
            raise forms.ValidationError("Employee ID already exists")
        return employee_id 
    
    def clean_username(self):       #username means Email
       
        username = self.cleaned_data['username']
        # if CustomUser.objects.filter(username=username).exists():
        #     raise forms.ValidationError("Email already exists")
        # if "@incedoinc.com" not in username:   
            # raise forms.ValidationError("Must be an Incedo Email address")
        return username

    def clean_name(self):       #username means Email
       
        name = self.cleaned_data['name']
        if any(char.isdigit() for char in name):
            raise forms.ValidationError("Name is not valid : Name cannot contain a digit.") 
        
        return name
    


class LoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=150, required = True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'password']   
