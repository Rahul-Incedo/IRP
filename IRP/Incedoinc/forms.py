from django.core import validators
from django import forms
from .models import Candidate, Job

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
        fields = ['requisition_id', 'job_description', 'position_owner_id']