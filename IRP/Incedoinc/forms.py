from django.core import validators
from django import forms
from django.forms.fields import IntegerField
from .models import Candidate, Job, TestModel, Employee, Feedback, Field, JD

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# from .models.Feedback import Field

class ResumeForm(forms.ModelForm):
    pdf_validator = validators.FileExtensionValidator(
        allowed_extensions=['pdf', 'doc', 'docx']
    )
    resume = forms.FileField(label='*Upload Resume (pdf, doc, and docx extensions are supported)', validators = [pdf_validator])

    class Meta:
        model = Candidate
        fields = ['resume']

class EditCandidateForm(forms.ModelForm):
    CGPA = forms.DecimalField(required=False,max_digits=5, decimal_places=3,
                            validators=[
                                validators.MinValueValidator(0),
                                validators.MaxValueValidator(10.0),
                            ]
    )
    mobile = forms.CharField(label='*Mobile No. (must be 10-digits)', required=True,
                            validators=[
                                validators.RegexValidator('^[0-9]{10}$',
                                    message='Mobile No. must be 10 digits'
                                )
                            ]
    )
    pdf_validator = validators.FileExtensionValidator(
        allowed_extensions=['pdf', 'doc', 'docx']
    )
    resume = forms.FileField(label='*Upload Resume (pdf, doc, and docx extensions are supported)', validators = [pdf_validator])
    # notice_period = forms.DecimalField(label='*Notice Period (in Months.Days)',max_digits=5, decimal_places=2,
    #                         validators=[
    #                             validators.MinValueValidator(0),
    #                         ]
    #                 )
    # experience = forms.DecimalField(label='*Experience (in Years.Months)',max_digits=5, decimal_places=2,
    #                         validators=[
    #                             validators.MinValueValidator(0),
    #                         ]
    # )
    notice_period = forms.CharField(label='*Notice Period (in Months.Days)',
                        widget = forms.TextInput(
                            attrs={'placeholder':'(2.15) represents 2 Months and 15 Days'},
                        ),
                        validators = [
                            validators.RegexValidator(r'^[0-9]*(\.([0-9]|[1-2][0-9]))?$'),
                        ]
                    )

    experience = forms.CharField(label='*Experience (in Years.Months)',
                        widget = forms.TextInput(
                            attrs={'placeholder':'(1.10) represents 1 Year 10 Months'},
                        ),
                        validators = [
                            validators.RegexValidator(r'^[0-9]*(\.([0-9]|[1][0-1]))?$'),
                        ]
                )
    class Meta:
        model = Candidate
        fields = '__all__'
        exclude = ['DOB']
        labels = {
            'f_name': '*First Name',
            'm_name': 'Middle Name',
            'l_name': '*Last Name',
            'registered_by':'Registered By',
            'email': '*Email',
            'gender': '*Gender',
            'CGPA': 'CGPA(out of 10)',
            'college_name': 'College Name',
            'experience': '*Experience (in Years.Months)',
            'mobile': '*10-digit Mobile No.',
            'projects_link' : 'Project',
            # 'DOB': 'Date of Birth',
            'notice_period': '*Notice Period (in Months.Days)',
            'resume': '*Upload Resume (pdf, doc, and docx extensions are supported)',
        }

class CandidateForm(forms.ModelForm):
    CGPA = forms.DecimalField(required=False,max_digits=5, decimal_places=3,
                            validators=[
                                validators.MinValueValidator(0),
                                validators.MaxValueValidator(10.0),
                            ]
    )
    mobile = forms.CharField(label='*Mobile Number (10 digits)', required=True,
                            validators=[
                                validators.RegexValidator('^[0-9]{10}$',
                                    message='Mobile Number must be 10 digits'
                                )
                            ]
    )
    pdf_validator = validators.FileExtensionValidator(
        allowed_extensions=['pdf', 'doc', 'docx']
    )
    # resume = forms.FileField(label='*Upload Resume (pdf, doc, and docx extensions are supported)', validators = [pdf_validator])
    requisition_id = forms.ModelChoiceField(Job.objects.all(), label='*Requisition ID')
    # notice_period = forms.DecimalField(label='*Notice Period (in Months.Days)',
    #                                     widget = forms.TextInput(
    #                                         attrs={'placeholder':'(2.15) represents 2 Months and 15 Days'},
    #                                     )
    #                 )
    notice_period = forms.CharField(label='*Notice Period (in Months.Days)',
                        widget = forms.TextInput(
                            attrs={'placeholder':'(2.15) represents 2 Months and 15 Days'},
                        ),
                        validators = [
                            validators.RegexValidator(r'^[0-9]*(\.([0-9]|[1-2][0-9]))?$'),
                        ]
                    )

    experience = forms.CharField(label='*Experience (in Years.Months)',
                        widget = forms.TextInput(
                            attrs={'placeholder':'(1.10) represents 1 Year 10 Months'},
                        ),
                        validators = [
                            validators.RegexValidator(r'^[0-9]*(\.([0-9]|[1][0-1]))?$'),
                        ]
                )
    class Meta:
        model = Candidate
        # fields = '__all__'
        fields = ['f_name', 'm_name', 'l_name', 'email', 'registered_by', 'gender', 'college_name', 'CGPA', 'college_name', 'experience', 'mobile', 'notice_period']
        # exclude = ['DOB']
        labels = {
            'f_name': '*First Name',
            'm_name': 'Middle Name',
            'l_name': '*Last Name',
            'email': '*Email',
            'gender': '*Gender',
            'college_name': 'College Name',
            'CGPA': 'CGPA(out of 10)',
            'experience': '*Experience (in months)',
            'mobile': '*10-digit Mobile No.',
            # 'DOB': 'Date of Birth',
            # 'resume': '*Upload Resume (pdf, doc, and docx extensions are supported)',
            'notice_period': '*Notice Period (in months)',
        }



class UploadJdForm(forms.ModelForm):
    extension_validator = validators.FileExtensionValidator(
        allowed_extensions=['pdf', 'doc', 'docx']
    )
    jd_file = forms.FileField(label='*Upload File (pdf, doc, and docx extensions are supported)', validators = [extension_validator])
    # jd_name = forms.CharField(label='*Name of Job Description')

    class Meta:
        model = JD
        fields = ['uploaded_by_employee', 'jd_file', 'jd_name']
        labels = {
            'jd_name' : '*Name of Job Description'
        }

class UploadJobForm(forms.ModelForm):
    jd = forms.ModelChoiceField(JD.objects.all(), label='*Select Job Description')
    class Meta:
        model = Job
        fields = ['requisition_id', 'raised_by_employee', 'position_owner_id', 'jd', 'requisition_status', 'total_positions', 'open_to_internal']
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
    # field_name = forms.CharField(max_length = 20, widget=forms.Select(choices=field_choices),)
    field_name = forms.CharField(max_length = 64, widget=forms.TextInput(attrs={'placeholder': 'Enter the field name'}))
    rating = forms.IntegerField(label = 'Rating (Out Of 5)', min_value=1, max_value=5)



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
