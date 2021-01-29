from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.http import HttpResponse

#include models
from .models import Job

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
    if request.method == 'POST':
        requisition_id = request.POST.get('requisition_id')
        return redirect(f'/search_jd/{requisition_id}')
    
    context={}
    return render(request,'home.html',context)


def search_jd_view(request, requisition_id):
    obj = Job.objects.get(requisitionId=requisition_id)
    context = {
        'file': obj.description
    }
    return render(request, 'jd_results.html', context)

# class Job(models.Model):
#     requisitionId = models.CharField(max_length=100, primary_key=True)
#     raisedByEmployee = models.ForeignKey(Employee, null = True, related_name='raisedByEmployee', on_delete=models.CASCADE)
#     positionOwner = models.ForeignKey(Employee, null = True, related_name='positionOwner', on_delete=models.CASCADE)
#     #positionOwner = models.ManyToOneField(Employee, blank=True, related_name='owner')

#     description = models.FileField()