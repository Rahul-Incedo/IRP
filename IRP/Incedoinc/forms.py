from django.core import validators
from django import forms
from .models import Candidate, Job, TestModel, Employee, JD

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
    resume = forms.FileField(label='*Upload Resume', validators = [pdf_validator])
    requisition_id = forms.ModelChoiceField(Job.objects.all(), required=True)
    class Meta:
        model = Candidate
        fields = '__all__'
        labels = {
            'f_name': '*First Name',
            'm_name': 'Middle Name',
            'l_name': '*Last Name',
            'email': '*Email',
            'gender': '*Gender',
            'CGPA': '*CGPA(out of 10)',
            'college_name': '*College Name',
            'experience': '*Experience',
            'mobile': '*10-digit Mobile No.',
            'DOB': '*Date of Birth',
            'resume': '*Upload Resume',
            'noticePeriod': '*Notice Period',
        }
    
class UploadJdForm(forms.ModelForm):
    pdf_validator = validators.FileExtensionValidator(
        allowed_extensions=['pdf']
    )
    jd_file = forms.FileField(label='*Upload File (pdf format is supported)', validators = [pdf_validator])
    class Meta:
        model = JD
        fields = ['uploaded_by_employee',  'jd_name', 'jd_file']
        label = {
            'uploaded_by_employee': 'Uploaded By',
            'jd_name': 'Job Description Name',
        }


class UploadJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['raised_by_employee', 'position_owner_id', 'requisition_id', 'jd_name']
        label = {
            'position_owner_id': '*Position Owner',
            'requisition_id': '*Requisition ID',
            'jd_name': '*Job Description',
        }

class TestForm(forms.ModelForm):
    class Meta:
        model = TestModel
        fields = ['field1', 'field2']



 
