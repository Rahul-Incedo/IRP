from django import forms
from .models import Candidate
class Candidate_details_form(forms.Form):
    email = forms.EmailField(label='Email', required=True)
    f_name = forms.CharField(label='First Name')
    m_name = forms.CharField(label='Middle Name', required=False)
    l_name = forms.CharField(label='Last Name')
    total_experience = forms.IntegerField(label='Total Experience (in years)', required=False)
    college_name = forms.CharField(label='College/University Name')
    cgpa = forms.DecimalField(label='CGPA (upto Current Semester)')
    grad_year = forms.IntegerField(label='Graduation Year')
    notice_period = forms.IntegerField(label='Notice Period of previous Employer (in months)', required=False)
    resume = forms.FileField(label='Select Resume', required=False)

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        if not email.endswith('.com'):
            raise forms.ValidationError('not a valid email')
        return email
    def clean_cgpa(self, *args, **kwargs):
        cgpa = self.cleaned_data.get('cgpa')
        if not (cgpa >= 0 and cgpa <= 10):
            raise forms.ValidationError('cgpa should be in within 0.0 to 10.0')
        return cgpa

    def clean_resume(self, *args, **kwargs):
        file = self.cleaned_data.get('resume')
        if (file is not None) and (not file.name.endswith('.pdf')):
            raise forms.ValidationError('Only pdf format is supported')
        return file




class CandidateForm(forms.ModelForm):
    email = forms.EmailField(label='Email', required=True)
    f_name = forms.CharField(label='First Name')
    m_name = forms.CharField(label='Middle Name', required=False)
    l_name = forms.CharField(label='Last Name')
    total_experience = forms.IntegerField(label='Total Experience (in years)', required=False)
    college_name = forms.CharField(label='College/University Name')
    cgpa = forms.DecimalField(label='CGPA (upto Current Semester)')
    grad_year = forms.IntegerField(label='Graduation Year')
    notice_period = forms.IntegerField(label='Notice Period of previous Employer (in months)', required=False)
    resume = forms.FileField(label='Select Resume', required=False)
    class Meta:
        model = Candidate
        fields = []
    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        if not email.endswith('.com'):
            raise forms.ValidationError('not a valid email')
        return email
    def clean_cgpa(self, *args, **kwargs):
        cgpa = self.cleaned_data.get('cgpa')
        if not (cgpa >= 0 and cgpa <= 10):
            raise forms.ValidationError('cgpa should be in within 0.0 to 10.0')
        return cgpa

    def clean_resume(self, *args, **kwargs):
        file = self.cleaned_data.get('resume')
        if (file is not None) and (not file.name.endswith('.pdf')):
            raise forms.ValidationError('Only pdf format is supported')
        return file

class Upload_jd_form(forms.Form):
    jd = forms.FileField(label='Select JobDescription')
    pos_owner_name = forms.CharField(label='Name of Position owner')
    pos_owner_emp_code = forms.IntegerField(label='EmloyeeCode of Position owner')

    def clean_jd(self):
        file = self.cleaned_data.get('jd')
        if (file is not None) and (not file.name.endswith('.pdf')):
            raise forms.ValidationError('Only pdf type is supported')
        return file
