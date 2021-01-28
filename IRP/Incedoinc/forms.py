from django import forms

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
        filename = self.data.get('resume')
        if filename != '' and not filename.endswith('.pdf'):
            raise forms.ValidationError('Resume should be pdf file')
        return self.cleaned_data
