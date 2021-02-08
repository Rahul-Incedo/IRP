from django.core import validators
from django import forms
from .models import Candidate, Job, TestModel, Employee, Feedback, Field, JD

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# from .models.Feedback import Field

class CandidateForm(forms.ModelForm):
    CGPA = forms.DecimalField(required=False,max_digits=5, decimal_places=3,
                            validators=[
                                validators.MinValueValidator(0),
                                validators.MaxValueValidator(10.0),
                            ]
    )
    pdf_validator = validators.FileExtensionValidator(
        allowed_extensions=['pdf', 'doc', 'docx']
    )
    resume = forms.FileField(label='*Upload Resume (pdf, doc, and docx extensions are supported)', validators = [pdf_validator])
    requisition_id = forms.ModelChoiceField(Job.objects.all(), label='*Requisition ID')
    notice_period = forms.IntegerField(label='*Notice Period',
                                        widget = forms.TextInput(
                                            attrs={'placeholder':'enter in months'},
                                        )
                    )
    class Meta:
        model = Candidate
        fields = '__all__'

class UploadJdForm(forms.ModelForm):
    pdf_validator = validators.FileExtensionValidator(
        allowed_extensions=['pdf', 'doc', 'docx']
    )
    jd_file = forms.FileField(label='*Upload File (pdf, doc, and docx extensions are supported)', validators = [pdf_validator])
    jd_name = forms.CharField(label='*Name of Job Description')

    class Meta:
        model = JD
        fields = ['uploaded_by_employee',  'jd_name', 'jd_file']
        label = {
        }

class UploadJobForm(forms.ModelForm):
    jd = forms.ModelChoiceField(JD.objects.all(), label='*Select Job Description')
    class Meta:
        model = Job
        fields = ['raised_by_employee', 'position_owner_id', 'requisition_id', 'jd']
        label = {
            'position_owner_id': '*Position Owner',
            'requisition_id': '*Requisition ID',
        }

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
    field_choices = [   ('', '------'),
                        ('Python', 'Python'),
                        ('Java', 'Java'),
                        ('C++', 'C++'),
                        ('C', 'C'),
                        ('PHP', 'PHP'),
                        ('SQL', 'SQL'),
                        ('JAVA script', 'JAVA script'),
                        ('Cloud Computing', 'Cloud Computing'),
                        ('Linux', 'Linux'),
                        ('Image Processing', 'Image processing'),
                        ('HTML', 'HTML'),
                        ('CSS', 'CSS'),
                        ('Kotlin', 'Kotlin'),
                        ('AWS', 'AWS'),
                        ('Neural Networks', 'Neural Networks'),
                        ('Deep Learning', 'Deep Learning'),
                        ('Machine learning', 'Machine learning'),
                        ('.NET', '.NET')]
    field_name = forms.CharField(max_length = 20, widget=forms.Select(choices=field_choices),)
    rating = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Field
        fields = '__all__'

    def clean_field_name(self):
        field_name = self.cleaned_data['field_name']
        f = self.cleaned_data['feedback_id']
        # f_obj = Feedback.objects.get(feedback_id=f)
        field_objects = Field.objects.all().filter(feedback_id=f)
        field_names = [obj.field_name for obj in field_objects]

        if field_name in field_names :
            raise forms.ValidationError("You have already reviewed this field")
        return field_name
