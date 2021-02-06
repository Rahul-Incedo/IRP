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
                        ('Cotlin', 'Cotlin'),
                        ('AWS', 'AWS'),
                        ('Neural Networks', 'Neural Networks'),
                        ('Deep Learning', 'Deep Learning'),
                        ('machine learning', 'machine learning'),
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
            raise forms.ValidationError("You have already reviewed this field, please choose the different field")
        return field_name

        # class ContactForm(forms.Form):
        #     # Everything as before.
        #     ...
        #
        #     def clean_recipients(self):
        #         data = self.cleaned_data['recipients']
        #         if "fred@example.com" not in data:
        #             raise ValidationError("You have forgotten about Fred!")
        #
        #         # Always return a value to use as the new cleaned data, even if
        #         # this method didn't change it.
        #         return data
