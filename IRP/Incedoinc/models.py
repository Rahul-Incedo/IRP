from django.db import models
import os

# Create your models here.
class Employee(models.Model):
    full_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=254, null=True)
    employee_id = models.CharField(max_length=64, primary_key=True, default=None)
    # password = models.CharField(max_length=64)
    # temp_password = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return f'{self.full_name}'


class JD(models.Model):
    jd_name = models.CharField(max_length=64, primary_key=True)
    jd_file = models.FileField(upload_to='JD/')
    uploaded_by_employee = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.jd_name}'
    def get_file_name(self):
        file_name = self.jd_file.name
        print(file_name)
        return file_name.lstrip('JD').lstrip('/')

#different requisition_id are mapped to one job_description
class Job(models.Model):
    requisition_id = models.CharField(max_length=64, primary_key=True)
    raised_by_employee = models.ForeignKey(Employee, related_name='raised_by_employee', null = True, on_delete=models.CASCADE)
    position_owner_id = models.ForeignKey(Employee, related_name='position_owner', null = True, on_delete=models.CASCADE)
    jd = models.ForeignKey(JD, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.requisition_id}'


class Candidate(models.Model):
    registered_by = models.ForeignKey(Employee, null =True, on_delete = models.CASCADE )
    f_name = models.CharField(max_length=64)
    m_name = models.CharField(max_length=64, null=True, blank=True)
    l_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=254, primary_key=True)
    gender_choice = [('M', 'Male'),
                    ('F', 'Female'),
                    ('O', 'Other')]
    gender = models.CharField(max_length=1,
                            choices= gender_choice)

    college_name = models.CharField(max_length = 254, null=True, blank=True)
    CGPA = models.DecimalField(null=True, max_digits=5, decimal_places=3)
    experience = models.DecimalField(decimal_places=3 , max_digits=5)
    mobile = models.CharField(max_length=10)
    DOB = models.DateField(null=True, blank=True)
    projects_link = models.URLField(null=True, blank=True)
    resume = models.FileField(upload_to='Resume/')
    notice_period = models.DecimalField(decimal_places=3 , max_digits=5)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def full_name(self):
        if self.m_name is not None:
    	    return f'{self.f_name} {self.m_name} {self.l_name}'
        else:
            return f'{self.f_name} {self.l_name}'

    def __str__(self):
        return f'{self.f_name} : {self.email}'


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    candidate_email = models.ForeignKey(Candidate, blank=True, null=True, on_delete=models.CASCADE)
    interviewer_id = models.ForeignKey(Employee, blank=True, null=True, on_delete=models.CASCADE)
    requisition_id = models.ForeignKey(Job, blank=True, on_delete = models.CASCADE)
    level = models.IntegerField(null=True)
    status_choices = [('pass', 'pass'),
                        ('fail', 'fail'),
                        ('pending', 'pending'),]
    status = models.CharField(choices = status_choices, max_length=10)
    comments = models.TextField(max_length=500, null=True, blank=True)
    interview_date = models.DateField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.status} {self.level}'

class Field(models.Model):
    field_id = models.AutoField(primary_key=True)
    feedback_id = models.ForeignKey(Feedback, null=True, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=20, null=False)
    rating = models.IntegerField(null=True, blank=True)
    comments = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.field_name}'


class TestModel(models.Model):
    field1 = models.CharField(blank=True, max_length=100)
    field2 = models.CharField(default=100, max_length=100)
