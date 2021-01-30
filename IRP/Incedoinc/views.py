from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from datetime import datetime

#include models
from .models import Employee, Job, Candidate, Feedback

#include forms
from .forms import CandidateForm, UploadJdForm


# Create your views here.
def index(request):
    return HttpResponse('<h1>Welcome to Incedo Recruitment Portal<h1>')
    
def add_candidate_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            form = CandidateForm()
    else:
        form = CandidateForm()
    context = {
        'form':form
    }
    return render(request, 'add_candidate.html', context)

def upload_jd_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = UploadJdForm(request.POST, request.FILES)
        if form.is_valid():
            print('_____submitted_form_is_valid______')
            form = UploadJdForm()
            form.save()
    else:
        form = UploadJdForm()
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


# def search_jd_view(request, requisition_id):
#     try:
#         obj = Job.objects.get(requisitionId=requisition_id)
#         context = {
#             'obj': obj
#         }
#     except Exception:
#         raise Http404("JD is not exist")
#     return render(request, 'jd_results.html', context)

def search_jd_view(request, requisition_id):
    obj = Job.objects.get(requisition_id=requisition_id)
    if obj is not None:
        context = {
            'obj': obj
        }
        return render(request, 'jd_results.html', context)
    else:
        raise Http404("JD is not exist")


def search_candidate(request):
    return HttpResponseRedirect(reverse("feedback", args=('python_1', 'rudra@gmail.com', 3)))

def feedback(request, req_id, email_id, level):
    if request.method == "POST":
        #candidate_email = Candidate.objects.get()
        #candidate_email = Candidate.objects.get(emailId='rudra@gmail.com')
        #interviewer_code = Employee.objects.get(incedoCode=201201)
        #time_stamp = datetime.timestamp(datetime.now())

        requisition_id = 'req_id'
        candidate_email = request.POST['candidate_email']
        interviewer_code = request.POST['interviewer_code']
        status = request.POST['status']
        rating_python = request.POST['rating_python']
        rating_java = request.POST['rating_java']
        rating_cpp = request.POST['rating_cpp']
        rating_sql = request.POST['rating_sql']
        comments = request.POST['comments']

        Feedback.objects.create(candidateEmail=Candidate.objects.get(emailId=candidate_email),
                                interviewerCode=Employee.objects.get(incedoCode=interviewer_code),
                                level=int(level)+1,
                                status=status,
                                ratingPython=rating_python,
                                ratingJava=rating_java,
                                ratingCPP=rating_cpp,
                                ratingSQL=rating_sql,
                                comments=comments,)
        return HttpResponseRedirect(reverse('test_name'))

    try:
        basic_detail={'Name' :'candidate_name',
                    'Email':email_id,
                    'Graduation_CGPA':'candidate_cgpa',
                    'University_name':'candidate_college_name'}

        if(level == 1):
             prv_feedback[level] = None

        if(level == 2):
            level_1 = { 'staus':'pass',
                        'python_rating':'python_rating',
                        'java_rating':'java_rating',
                        'cpp_rating': 'cpp_rating',
                        'sql_rating': 'sql_rating',
                        'comments' : 'comments'}

            context = {
                'basic_detail':basic_detail,
                'level_1': level_1,
            }

        if(level == 3):
            level_1 = { 'staus':'pass',
                        'python_rating':'python_rating',
                        'java_rating':'java_rating',
                        'cpp_rating': 'cpp_rating',
                        'sql_rating': 'sql_rating',
                        'comments' : 'comments'}

            level_2 = { 'staus':'pass',
                        'python_rating':'python_rating',
                        'java_rating':'java_rating',
                        'cpp_rating': 'cpp_rating',
                        'sql_rating': 'sql_rating',
                        'comments' : 'comments'}
            context = {
                'basic_detail':basic_detail,
                'level_1': level_1,
                'level_2': level_2,
            }

    except Feedback.DoesNotExist:
        raise Http404('Feedback does not exist')

    return render(request, 'registration/feedback.html', context)


def test(request):
    return HttpResponse('inside the test')
