from django.core import validators
from django import forms
from .models import Candidate, Job, TestModel, Employee, Feedback, Field

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
# from .models.Feedback import Field

class CandidateForm(forms.ModelForm):
    CGPA = forms.DecimalField(max_digits=5, decimal_places=3,
                            validators=[
                                validators.MinValueValidator(0),
                                validators.MaxValueValidator(10.0),
                            ]
    )
    pdf_validator = validators.FileExtensionValidator(
        allowed_extensions=['pdf']
    )
    resume = forms.FileField(validators = [pdf_validator])
    requisition_id = forms.ModelChoiceField(Job.objects.all(), required=True)
    class Meta:
        model = Candidate
        fields = '__all__'

class UploadJdForm(forms.ModelForm):
    pdf_validator = validators.FileExtensionValidator(
        allowed_extensions=['pdf']
    )

    job_description = forms.FileField(validators = [pdf_validator])
    class Meta:
        model = Job
        fields = ['raised_by_employee', 'requisition_id', 'job_description', 'position_owner_id']

class TestForm(forms.ModelForm):
    class Meta:
        model = TestModel
        fields = ['field1', 'field2']



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

class FieldForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Field
        fields = '__all__'
