from django.shortcuts import render
from django.http import HttpResponse

from .models import Employee, Job, Candidate, Feedback, CandidateJobInfo

# Create your views here.
def index(request):
    return HttpResponse('Welcome to Incedo Portal')
