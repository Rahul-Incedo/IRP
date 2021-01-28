from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import HttpResponse



#include forms
from .forms import Candidate_details_form, Upload_jd_form


# Create your views here.
def index(request):
    return HttpResponse('Welcome to Incedo Portal')
    
def add_candidate_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = Candidate_details_form(request.POST, request.FILES)
        if form.is_valid():
            form = Candidate_details_form()
    else:
        form = Candidate_details_form()
    context = {
        'form':form
    }
    return render(request, 'add_candidate.html', context)

def upload_jd_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = Upload_jd_form(request.POST, request.FILES)
        if form.is_valid():
            print('_____submitted_form_is_valid______')
            form = Upload_jd_form()
    else:
        form = Upload_jd_form()
    context = {
        'form' : form
    }
    return render(request, 'upload_jd.html', context)
    
def home(request):
    context={}
    return render(request,'home.html',context)
