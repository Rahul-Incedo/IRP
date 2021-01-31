from django.db import models
from django.contrib.auth import User
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=64)
    emailId = models.EmailField(max_length=254, null=True)
    incedoCode = models.CharField(max_length=64, primary_key=True, default=None)
    password = models.CharField(max_length=64)
    tempPassword = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class Job(models.Model):
    requisitionId = models.CharField(max_length=100, primary_key=True)
    raisedByEmployee = models.ForeignKey(Employee, null = True, related_name='raisedByEmployee', on_delete=models.CASCADE)
    positionOwner = models.ForeignKey(Employee, null = True, related_name='positionOwner', on_delete=models.CASCADE)
    #positionOwner = models.ManyToOneField(Employee, blank=True, related_name='owner')

    description = models.FileField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f'{self.description}'

class Candidate(models.Model):
    firstName = models.CharField(max_length=64 )
    middleName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=64 )
    requisitionId = models.ForeignKey(Job, null=True, on_delete = models.CASCADE)
    registeredBy = models.ForeignKey(Employee, null =True, on_delete = models.CASCADE )
    emailId = models.EmailField(max_length=254, primary_key=True)
    gender_choice = [('M', 'Male'),
                    ('F', 'Female')]
    gender = models.CharField(max_length=1,
                            choices= gender_choice)
    universityRollNo = models.CharField(max_length=64 )
    graduationCGPA = models.FloatField(null=True)
    graduationYear = models.IntegerField(null=True)
    collegeName = models.CharField(max_length = 254 )
    experience = models.IntegerField(null=True)
    mobileNo = models.CharField(max_length=10)
    DOB = models.DateField(auto_now = True)
    projectsLink = models.URLField(null=True)
    resume = models.FileField(upload_to=None, max_length=100)#path for saving the resume
    noticePeriod = models.IntegerField(null=True)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f'{self.firstName} {self.lastName} : {self.emailId}'


class Feedback(models.Model):
    feedbackId = models.AutoField(primary_key=True)
    candidateEmail = models.ForeignKey(Candidate, blank=True, null=True, on_delete=models.CASCADE)
    interviewerCode = models.ForeignKey(Employee, blank=True, null=True, on_delete=models.CASCADE)
    requisitionId = models.ForeignKey(Job, blank=True, on_delete = models.CASCADE)
    level = models.IntegerField(null=True)
    status_choices = [('P', 'pass'),
                        ('F', 'fail')]
    status = models.CharField(max_length=4, choices = status_choices)
    ratingPython = models.IntegerField(null=True)
    ratingJava = models.IntegerField(null=True)
    ratingCPP = models.IntegerField(null=True)
    ratingSQL = models.IntegerField(null=True)
    comments = models.TextField(max_length=500, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Result for {self.candidateEmail} at level {self.level} is {self.status}'






   
'''
class CandidateJobInfo(models.Model):
    jobInfoId =  models.AutoField(primary_key=True)
    emailId = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    requisitionId = models.ForeignKey(Job, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.jobInfoId}'

'''



'''
class CandidateJobInfo(models.Model):
    jobInfoId =  models.AutoField(primary_key=True)
    emailId = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    requisitionId = models.ForeignKey(Job, on_delete = models.CASCADE)
    level1 = models.ForeignKey(Feedback, related_name='level1', null=True, on_delete = models.CASCADE)
    level2 = models.ForeignKey(Feedback, related_name='level2', null=True, on_delete = models.CASCADE)
    level3 = models.ForeignKey(Feedback, related_name='level3', null=True, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.jobInfoId}'
        '''
