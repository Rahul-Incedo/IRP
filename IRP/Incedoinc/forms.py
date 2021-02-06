from django.core import validators
from django import forms
from .models import Candidate, Job, TestModel, Employee, JD

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
        labels = {
            'f_name': '*First Name',
            'm_name': 'Middle Name',
            'l_name': '*Last Name',
            'email': '*Email',
            'gender': '*Gender',
            'college_name': 'College Name',
            'CGPA': 'CGPA(out of 10)',
            'experience': '*Experience',
            'mobile': '*10-digit Mobile No.',
            'DOB': 'Date of Birth',
            'resume': '*Upload Resume (pdf, doc, and docx extensions are supported)',
            'noticePeriod': '*Notice Period',
        }
    
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
