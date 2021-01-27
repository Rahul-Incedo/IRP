from django import forms


class Candidate_details_form(forms.Form):
    email = forms.EmailField(label='Email', required=True)
    f_name = forms.CharField(label='First Name')
    m_name = forms.CharField(label='Middle Name', required=False)
    l_name = forms.CharField(label='Last Name')
    total_experience = forms.IntegerField(label='Total Experience (in years)', required=False)
    college_name = forms.CharField(label='College/University Name')
    cgpa = forms.DecimalField(label='CGPA (upto Current Semester)')
    grad_year = forms.DateField(label='Graduation Year')
    notice_period = forms.IntegerField(label='Notice Period of previous Employer (in months)', required=False)
    resume = forms.FileField(label='Select Resume', required=False)
