from django.db import models

# Create your models here.
class Employee(models.Model):
    full_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=254, null=True)
    employee_id = models.CharField(max_length=64, primary_key=True, default=None)
    password = models.CharField(max_length=64)
    temp_password = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return f'{self.full_name}'


class Job(models.Model):
    requisition_id = models.CharField(max_length=64, primary_key=True)
    raised_by_employee = models.ForeignKey(Employee, null = True, related_name='raisedByEmployee', on_delete=models.CASCADE)
    position_owner_id = models.ForeignKey(Employee, null = True, related_name='positionOwner', on_delete=models.CASCADE)
    job_description = models.FileField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.requisition_id}'


class Candidate(models.Model):
    f_name = models.CharField(max_length=64)
    m_name = models.CharField(max_length=64, null=True, blank=True)
    l_name = models.CharField(max_length=64)
    registered_by = models.ForeignKey(Employee, null =True, on_delete = models.CASCADE )
    email = models.EmailField(max_length=254, primary_key=True)
    gender_choice = [('M', 'Male'),
                    ('F', 'Female')]
    gender = models.CharField(max_length=1,
                            choices= gender_choice)

    CGPA = models.DecimalField(null=True, max_digits=5, decimal_places=3)
    college_name = models.CharField(max_length = 254)
    experience = models.IntegerField(null=True)
    mobile = models.CharField(max_length=10)
    DOB = models.DateField(auto_now = True)
    projects_link = models.URLField(null=True, blank=True)
    resume = models.FileField()
    noticePeriod = models.IntegerField(null=True)
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
    rating_python = models.IntegerField(null=True, blank=True)
    rating_java = models.IntegerField(null=True, blank=True)
    rating_cpp = models.IntegerField(null=True, blank=True)
    rating_sql = models.IntegerField(null=True, blank=True)
    comments = models.TextField(max_length=500, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.status}'


class TestModel(models.Model):
    field1 = models.CharField(blank=True, max_length=100)
    field2 = models.CharField(default=100, max_length=100)
