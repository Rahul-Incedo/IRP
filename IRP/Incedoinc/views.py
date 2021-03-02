from django.core.exceptions import ValidationError
from django.db.models import query , Q
from django.shortcuts import redirect, render
from decimal import Context
from django.contrib.auth.backends import UserModel
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import LoginForm, SignUpForm, FieldForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

UserModel = get_user_model()
from .forms import SignUpForm
import os
import pdfkit
from datetime import date as date_
# Vaishnavi changed authentication

#include models
from .models import Employee, Job, Candidate, Feedback, Field, JD, RequisitionCandidate
from .models import TestModel

#include forms
from .forms import CandidateForm, UploadJdForm, UploadJobForm , EditCandidateForm
from .forms import TestForm

from django.conf import settings

# Create ur views here.
def test_view(request, **kwargs):
    print(request.GET)
    if 'delete_button' in request.GET:
        print('delete_signal')
        return render(request, 'test.html', {'delete_signal': 'true'})
    return render(request, 'test.html', {})
    return HttpResponse('<h1> test page </h>')
def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return HttpResponseRedirect(reverse('first_page'))

def delete_jd_view(request, jd_pk):
    query = JD.objects.get(pk=jd_pk)
    jd_name = query.jd_name
    query.jd_file.delete()
    query.delete()
    return redirect('/manage-jd/?deleted='+jd_name)

def delete_job_view(request, job_pk):
    query = Job.objects.get(pk=job_pk)
    requisition = query.requisition_id

    candidate_list_tuple = list(set(Feedback.objects.filter(requisition_id=requisition).values_list('candidate_email').order_by('-candidate_email')))
    candidate_list=[x[0] for x in candidate_list_tuple]
    for c in candidate_list:
        candidate_obj=Candidate.objects.filter(email=c)
        candidate_obj[0].resume.delete()
        candidate_obj[0].delete()

    query.delete()
    return redirect('/manage-job/?deleted='+requisition)

def view_jd_view(request, jd_pk):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        pass
    context = {
        'obj' : JD.objects.get(pk=jd_pk)
    }
    return render(request, 'view_jd.html', context)

def view_job_view(request, job_pk):
    if not request.user.is_authenticated:
        return redirect('login')
    if 'edit' in request.GET:
        return redirect('../edit/')
    job_object = Job.objects.get(pk=job_pk)
    # candidate_set = set(Feedback.objects.filter(requisition_id=job_pk).values_list('candidate_email'))
    # offered_count = 0
    # for candidate in candidate_set:
    #     if candidate.status == ''
    # open_positions = job_object.total_positions-len(RequisitionCandidate.objects.filter(candidate_status='offered'))
    context = {
        'obj' : job_object,
    }
    return render(request, 'view_job.html', context)

def edit_job_view(request, job_pk):
    if not request.user.is_authenticated:
        return redirect('login')

    if 'cancel' in request.GET:
        return redirect('../view/')

    job_object = Job.objects.get(requisition_id=job_pk)
    form = UploadJobForm(request.POST or None, instance=job_object)
    form.fields['raised_by_employee'].disabled = True
    form.fields['requisition_id'].disabled = True

    if form.is_valid():
        job_object = form.save(commit=False)
        job_object.timestamp_updated = datetime.now()
        job_object.save()
        return redirect('../view/')
        return HttpResponse('<h1>save success</h1>')
    context = {
        'form' : form
    }
    return render(request, 'edit_job.html', context)

def manage_jd_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')
    user = Employee.objects.get(email=request.user.username)
    if request.method == 'GET' and 'jd_name' in request.GET:
        search_query = request.GET['jd_name']
        query_set = JD.objects.filter(jd_name = search_query)
        context = {
            'query_set' : query_set
        }
        return render(request, 'manage_jd.html', context)
    elif request.method == 'GET' and 'deleted' in request.GET:
        msg = 'JD ( '+request.GET['deleted']+' ) is deleted'
        context = {
            'msg' : msg
        }
        return render(request, 'manage_jd.html', context)
    if request.method == 'POST':
        if 'home_button' in request.POST:
            return redirect('home_page')
        elif 'search_button' in request.POST:
            search_query = request.POST['search_query']
            if search_query is '':
                query_set = None
                msg = 'Enter something to search'
            else:
                query_set = JD.objects.filter(Q(jd_name__icontains=search_query)
                                            | Q(uploaded_by_employee__full_name__icontains=search_query)
                            ).distinct()
                msg = None
            context = {
                'query_set': query_set,
                'msg' : msg,
            }
            return render(request, 'manage_jd.html', context)
        elif 'list_all_button' in request.POST:
            query_set = JD.objects.all()
            context = {
                'query_set': query_set
            }
            return render(request, 'manage_jd.html', context)
        elif 'upload_jd_button' in request.POST:
            return redirect('upload_jd_page')
        elif 'delete_jd_button' in request.POST:
            return HttpResponse('<h1>delete jd</h1>')

    return render(request, 'manage_jd.html/', {})

    return HttpResponse('<h1>this is managejd</h1>')


def manage_job_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return render(request, 'login')
    if request.method == 'GET' and 'requisition_id' in request.GET:
        search_query = request.GET['requisition_id']
        query_set = Job.objects.filter(requisition_id = search_query)
        context = {
            'query_set' : query_set
        }
        return render(request, 'manage_job.html', context)
    elif request.method == 'GET' and 'expand_token' in request.GET:
        expand_token = request.GET['expand_token']
        query_set = Job.objects.all()
        context = {
            'query_set' : query_set,
            'expand_token' : expand_token,
            'sub_query_set' : RequisitionCandidate.objects.filter(requisition_id=expand_token)
        }
        return render(request, 'manage_job.html', context)
    elif request.method == 'GET' and 'deleted' in request.GET:
        msg = 'Requisition ( '+request.GET['deleted']+' ) is Deleted'
        context = {
            'msg' : msg
        }
        return render(request, 'manage_job.html', context)
    if request.method == 'POST':
        if 'home_button' in request.POST:
            return redirect('home_page')
        if 'search_button' in request.POST:
            search_query = request.POST['search_query']
            if search_query is '':
                query_set = None
                msg = 'Enter something to search'
            else:
                query_set = Job.objects.filter( Q(requisition_id__icontains=search_query)
                                            | Q(jd__jd_name__icontains=search_query)
                                            | Q(requisitioncandidate__candidate_email__f_name__icontains=search_query)
                                            | Q(position_owner_id__full_name__icontains=search_query)
                                            | Q(raised_by_employee__full_name__icontains=search_query)
                                            | Q(requisition_status__exact = search_query)
                            ).distinct()
                msg = None
            context = {
                'query_set': query_set,
                'msg' : msg,
            }
            return render(request, 'manage_job.html', context)
        elif 'list_all_button' in request.POST:
            query_set = Job.objects.all()
            context = {
                'query_set': query_set,
            }
            return render(request, 'manage_job.html', context)
        elif 'raise_requisition_button' in request.POST:
            return redirect('upload_job_page')

    return render(request, 'manage_job.html/', {})

    return HttpResponse('<h1>this is managejd</h1>')

def upload_jd_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")
    username = request.user.username
    user = Employee.objects.get(email=username)
    if request.method == 'POST':
        #if someone forcefully entered raised_by_field using tampering of form
        if 'uploaded_by_employee' in request.POST:
            raise ValidationError('FORM IS TAMPERED')
        # print(request.POST)
        form = UploadJdForm(request.POST, request.FILES, initial={'uploaded_by_employee':user})
        form.fields['uploaded_by_employee'].disabled = True
        if form.is_valid():
            obj = form.save(commit=False)
            # file_name = obj.get_file_name()
            # file_name = file_name.replace('.pdf', '').replace('.docx', '').replace('.doc', '')
            # obj.jd_name = file_name
            obj.timestamp = datetime.now()
            obj.save()
            response = redirect('/manage-jd/?jd_name='+obj.jd_name)
            return response
            # return custom_redirect('manage_jd_page', arg1='dfo')
    else:
        form = UploadJdForm(initial={'uploaded_by_employee':user})
        form.fields['uploaded_by_employee'].disabled = True
    context = {
        'form' : form
    }
    return render(request, 'forms/upload_jd.html', context)


def upload_job_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')
    username = request.user.username
    user = Employee.objects.get(email=username)
    if request.method == 'POST':
        #if someone forcefully entered raised_by_field using tampering of form
        if 'raised_by_employee' in request.POST:
            raise ValidationError('FORM IS TAMPERED')
        # print(request.POST)
        form = UploadJobForm(request.POST, initial={'raised_by_employee':user})
        form.fields['raised_by_employee'].disabled = True
        if form.is_valid():
            obj = form.save(commit=False)
            obj.timestamp_created = datetime.now()
            obj.timestamp_updated = datetime.now()
            obj.save()
            return redirect('/manage-job/?requisition_id='+obj.requisition_id)
    else:
        form = UploadJobForm(initial={'raised_by_employee':user})
        form.fields['raised_by_employee'].disabled = True
    context = {
        'form' : form
    }
    return render(request, 'forms/upload_job.html', context)


def home_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        if 'search_requisition_id_button' in request.POST:
            requisition_id = request.POST.get('requisition_id')
            if len(requisition_id) >= 3:
                query_set = Job.objects.filter(requisition_id__contains=requisition_id)
            else:
                query_set = Job.objects.filter(requisition_id=requisition_id)
            context = {
                'requisition_id' : requisition_id,
                'query_set': query_set,
            }
            return render(request, 'home.html', context)
        elif 'manage_jd_button' in request.POST:
            return redirect('manage_jd_page')
        elif 'manage_job_button' in request.POST:
            return redirect('manage_job_page')
        elif 'manage_candidate_button' in request.POST:
            return redirect('search_candidate')
        elif 'referrals_button' in request.POST:
            return redirect('referrals_page')
        else:
            return Http404('Page Not Exist')
    return render(request,'home.html')


def add_candidate_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')

    user = Employee.objects.get(email=request.user.username)
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES, initial={'registered_by': user})
        form.fields['registered_by'].disabled = True

        if form.is_valid():
            candidate_obj = form.save()
            requisition_id = form.cleaned_data['requisition_id']

            candidate_email = form.cleaned_data['email']

            job_obj = Job.objects.get(requisition_id=requisition_id)
            Feedback.objects.create(
                candidate_email=candidate_obj,
                level=1,
                requisition_id=job_obj,
                status='pending',
            )
            Feedback.objects.create(
                candidate_email=candidate_obj,
                level=2,
                requisition_id=job_obj,
                status='pending',
            )
            Feedback.objects.create(
                candidate_email=candidate_obj,
                level=3,
                requisition_id=job_obj,
                status='pending',
            )
            RequisitionCandidate.objects.create(
                requisition_id = job_obj,
                candidate_email = candidate_obj,
                candidate_status = 'in_progress',
            )
            # return redirect('../search_candidate/', )
            return redirect('../'+'search_candidate/?candidate_email='+str(candidate_email))
    else:
        form = CandidateForm(initial={'registered_by': user})
        form.fields['registered_by'].disabled = True
    context = {
        'form': form
    }
    return render(request, 'forms/add_candidate.html', context)
########################################################################################3









#
# def login_view(request):
  #  username = request.POST['username']
 #   password = request.POST['password']
  #  print(username)

  #  user = authenticate(request, username=username, password=password)
  #  if user is not None:
   #     login(request, user)
  #      return HttpResponseRedirect(reverse('index'))
    #else:
 #       return render(request, "users/login.html", {"message":"Invalid credential"})






def dashboard(request):
    return render(request, "Signup_Login/dashboard.html")

# def dashboard(request):
#     return render(request, "SignUp_Login/dashboard.html")
def edit_candidate(request,candidate_email):
    if not request.user.is_authenticated:
        return redirect('login')
    if "cancel" in request.POST:
        return redirect('../../view_candidate/'+str(candidate_email))
    candidate_obj=Candidate.objects.filter(email=candidate_email)
    if len(candidate_obj)==0 :
            return render(request,'edit_candidate.html',{'error_msg':"Oops ;( Something went wrong"})
            prer
    form = EditCandidateForm(request.POST or None, request.FILES or None, instance=candidate_obj[0])
    form.fields['registered_by'].disabled = True
    form.fields['email'].disabled = True
    if form.is_valid():
        candidate_obj = form.save()
        return redirect('../../view_candidate/'+str(candidate_email))
    context = {
    'form': form
    }
    return render(request, 'edit_candidate.html', context)

def view_candidate(request,candidate_email):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':

        candidate_obj=Candidate.objects.filter(email=candidate_email)
        print(candidate_email)

        print("sdfsdfsdfsd------------------------------")
        return redirect('../../edit_candidate/'+str(candidate_email))

    candidate_obj=Candidate.objects.filter(email=candidate_email)
    if len(candidate_obj)==0 :
            return render(request,'view_candidate.html',{'error_msg':"Oops ;( Something went wrong"})

    f_name = candidate_obj[0].f_name
    if f_name==None:
        f_name=""

    m_name = candidate_obj[0].m_name
    if m_name==None:
        m_name=""

    l_name = candidate_obj[0].l_name
    if l_name==None:
        l_name=""

    registered_by = candidate_obj[0].registered_by
    if registered_by==None:
        registered_by=""

    email=candidate_obj[0].email
    if email==None:
        email=""

    gender=candidate_obj[0].gender
    if gender==None:
        gender=""

    CGPA=candidate_obj[0].CGPA
    if CGPA==None:
        CGPA=""

    college_name=candidate_obj[0].college_name
    if college_name==None:
        college_name=""

    experience=candidate_obj[0].experience
    if experience==None:
        experience=""

    mobile=candidate_obj[0].mobile
    if mobile==None:
        mobile=""

    projects_link=candidate_obj[0].projects_link
    if projects_link==None:
        projects_link=""

    notice_period=candidate_obj[0].notice_period
    if notice_period==None:
        notice_period=""

    resume_url=candidate_obj[0].resume.url
    resume_name=candidate_obj[0].resume.name[7:]

    timestamp=candidate_obj[0].timestamp
    if timestamp==None:
        timestamp=""

    requisition_candidate_temp_list_tuple = list(set(RequisitionCandidate.objects.filter(candidate_email=Candidate.objects.get(email=candidate_email))))
    # if len(requisition_candidate_temp_list_tuple)==0:
    #     return render(request, 'my_referrals.html',{'error_message':'Something Went Wrong'})
    requisition_candidate_context={}
    for x in range(len(requisition_candidate_temp_list_tuple)):
        requisition_candidate_context[x+1]=requisition_candidate_temp_list_tuple[x]

    context={
        'f_name':f_name,
        'm_name':m_name,
        'l_name':l_name,
        'registered_by':registered_by,
        'email':email,
        'gender':gender,
        'CGPA':CGPA,
        'college_name':college_name,
        'experience':experience,
        'mobile':mobile,
        'projects_link':projects_link,
        'notice_period':notice_period,
        'resume_url':resume_url,
        'resume_name':resume_name,
        'timestamp':timestamp,
        'requisition_candidate_context':requisition_candidate_context
    }

    return render(request,'view_candidate.html',context)

def search_candidate(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')
    if (request.GET and request.GET is not {}) or request.method == 'POST':
        context={}
        result=[]
        if request.method == 'POST':
            if 'home_button' in request.POST:
                return redirect('home_page')
            # print(request.POST)
            if 'listall' in request.POST:
                temp_candidate_list_tuple = list(set((Feedback.objects.all().values_list('candidate_email'))))
                temp_candidate_list=[x[0] for x in temp_candidate_list_tuple]
                temp_candidate_list.sort()
                if len(temp_candidate_list)==0:
                    return render(request, 'search.html',{'error_message':'Oops :(   No Candidate Yet'})
                print(temp_candidate_list,"--------------")
                # result=[]
                for candidate in temp_candidate_list:
                    temp_req_id_list_tuple = list(set(Feedback.objects.filter(candidate_email=candidate).values_list('requisition_id')))
                    temp_req_id_list=[x[0] for x in temp_req_id_list_tuple]
                    temp_req_id_list.sort(reverse=True)
                    print(candidate,"  :  ",temp_req_id_list)
                    for r in temp_req_id_list:
                         result.append([r,candidate])
                print (result)
                if len(result)==0 :
                    return render(request, 'search.html',{'error_message':'No Results'})
            elif 'dropdown' in request.POST:
                if request.POST['dropdown'] == 'req_id':
                    requisition_id=request.POST['search_element']
                    if len(requisition_id)==0:
                        return render(request, 'search.html',{'error_message':'Please enter something'})
                    temp_req_id_list=list(Job.objects.filter(requisition_id__contains=requisition_id))
                    if len(temp_req_id_list)==0 :
                         return render(request, 'search.html',{'error_message':'No matching Requition Id for \''+str(requisition_id)+'\''})

                    req_id_list=[x.requisition_id for x in temp_req_id_list]
                    req_id_list.sort()
                    # result=[]
                    print(req_id_list,"------------------------------")
                    for r in req_id_list:
                        temp_candidate_list_tuple = list(set(Feedback.objects.filter(requisition_id=r).values_list('candidate_email').order_by('-candidate_email')))
                        temp_candidate_list=[x[0] for x in temp_candidate_list_tuple]
                        temp_candidate_list.sort()
                        for c in temp_candidate_list:
                            result.append([r,c])
                        print(result)
                    if len(result)==0 :
                        return render(request, 'search.html',{'error_message':'No candidate(s) applied for Requition Id matching \''+str(requisition_id+'\'')})
                elif request.POST['dropdown'] == 'email':
                    candidate_email= request.POST['search_element']
                    if len(candidate_email)==0:
                        return render(request, 'search.html',{'error_message':'Please enter something'})
                    temp_candidate_list = list(Candidate.objects.filter(email__contains=candidate_email))
                    if len(temp_candidate_list)==0 :
                        return render(request, 'search.html',{'error_message':'No matching Candidate for \''+str(candidate_email)+'\''})
                    candidate_list=[x.email for x in temp_candidate_list]
                    candidate_list.sort()
                    # result=[]
                    for c in candidate_list:
                        print(c)
                        temp_req_id_list_tuple = list(set(Feedback.objects.filter(candidate_email=c).values_list('requisition_id').order_by('-requisition_id')))
                        temp_req_id_list=[x[0] for x in temp_req_id_list_tuple]
                        temp_req_id_list.sort()
                        for r in temp_req_id_list:
                            result.append([r,c])
                    print (result)
                    if len(result)==0 :
                        return render(request, 'search.html',{'error_message':'No results'})
        elif request.GET and request.GET is not {} :
            print('request.GET is not none')
            print(request.GET)
            candidate_email = ''
            # if kwargs:
            #     if 'candidate_email' not in kwargs:
            #         raise ValidationError('Get request has arguments type which are not supported')
            #     else:
            #         candidate_email = kwargs['candidate_email']
            if 'candidate_email' in request.GET:
                candidate_email = request.GET['candidate_email']
                print('request.GET',candidate_email)
            else:
                return render(request, 'search.html',{'error_message':'No Results'})

            if len(candidate_email)==0:
                return render(request, 'search.html',{'error_message':'Please enter something'})
            candidate_list = list(Candidate.objects.filter(email__contains=candidate_email))
            if len(candidate_list)==0 :
                return render(request, 'search.html',{'error_message':'No matching Candidate for \''+str(candidate_email)+'\''})
            for c in candidate_list:
                print(c.email)
                temp_req_id_list = list(set(Feedback.objects.filter(candidate_email=c).values_list('requisition_id').order_by('-requisition_id')))
                for r in temp_req_id_list:
                    result.append([r[0],c.email])
            print (result)
            if len(result)==0 :
                return render(request, 'search.html',{'error_message':'No matching Candidate for \''+str(candidate_email)+'\''})
        if len(result)==0 :
            return render(request, 'search.html',{'error_message':'No Results'})
        for x in range(len(result)):
            temp_dict={}
            # print(type(candidate_list[x][0]))
            l1_obj=Feedback.objects.get(requisition_id=result[x][0],candidate_email=result[x][1], level = 1)
            l2_obj=Feedback.objects.get(requisition_id=result[x][0],candidate_email=result[x][1], level = 2)
            l3_obj=Feedback.objects.get(requisition_id=result[x][0],candidate_email=result[x][1], level = 3)

            l1=Feedback.objects.get(requisition_id=result[x][0],candidate_email=result[x][1], level = 1).status
            l3=Feedback.objects.get(requisition_id=result[x][0],candidate_email=result[x][1], level = 3).status
            l2=Feedback.objects.get(requisition_id=result[x][0],candidate_email=result[x][1], level = 2).status
            status_dict = {
                'selected' : 'pass',
                'rejected' : 'fail',
                'pending' : 'pending',
            }
            l1 = status_dict[l1]
            l2 = status_dict[l2]
            l3 = status_dict[l3]

            l1_id = l1_obj.feedback_id
            l2_id = l2_obj.feedback_id
            l3_id = l3_obj.feedback_id

            temp_dict['req_id']=result[x][0];
            temp_dict['email']=result[x][1];
            temp_dict['resume'] = Candidate.objects.get(email=result[x][1]).resume
            level_=3
            level__ = 3
            if l1=='pending':
                temp_dict[1]='pending'
                temp_dict[2]='-'
                temp_dict[3]='-'
                level_=1
            elif l1=='fail':
                temp_dict[1]='fail'
                temp_dict[2]='NA'
                temp_dict[3]='NA'
                level__ = 1
            else :
                if l2=='pending':
                    temp_dict[1]='pass'
                    temp_dict[2]='pending'
                    temp_dict[3]='-'
                    level_=2
                elif l2=='fail':
                    temp_dict[1]='pass'
                    temp_dict[2]='fail'
                    temp_dict[3]='NA'
                    level__ = 2
                else :
                    if l3=='pending':
                        temp_dict[1]='pass'
                        temp_dict[2]='pass'
                        temp_dict[3]='pending'
                        level_=2
                    elif l3=='fail':
                        temp_dict[1]='pass'
                        temp_dict[2]='pass'
                        temp_dict[3]='fail'
                        level__ = 3
                    else:
                        temp_dict[1]='pass'
                        temp_dict[2]='pass'
                        temp_dict[3]='pass'
            context[str(x+1)]=temp_dict
        return render(request, 'search.html',{'context':context , 'level_':level_, 'level__':level__, 'l1_id':l1_id, 'l2_id':l2_id, 'l3_id':l3_id})
    else:
        print('else part')
        return render(request, 'search.html')

def feedback(request, req_id, email_id, level):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        status = request.POST['status']
        comments = request.POST['comments']
        interview_date = request.POST['interview_date']
        interviewer_id = Employee.objects.get(email=request.user._wrapped.username).employee_id

        feedback_object = Feedback.objects.get(candidate_email=email_id, requisition_id=req_id, level=level)
        feedback_object.status=status
        feedback_object.interviewer_id = Employee.objects.get(employee_id=interviewer_id)
        feedback_object.interview_date = interview_date
        feedback_object.comments = comments
        feedback_object.timestamp = datetime.now()
        feedback_object.save()

        candidate_email=email_id
        return redirect('../../../../search_candidate/?candidate_email='+str(candidate_email))

    '''GET part'''
    try:
        feedback_object = Feedback.objects.get(candidate_email=email_id, requisition_id=req_id, level=level)
        form = FieldForm(initial={'feedback_id' : feedback_object})
        form.fields['feedback_id'].widget = forms.HiddenInput()
        feedback_id = feedback_object.pk
        candidate_object = Candidate.objects.get(email=email_id)
        candidate_name = candidate_object.full_name
        candidate_cgpa = candidate_object.CGPA
        candidate_college_name =  candidate_object.college_name
        interviewer_id = Employee.objects.get(email=request.user._wrapped.username)

        current_field_object = Field.objects.all().filter(feedback_id = feedback_id)
        current_field_names = [obj.field_name for obj in current_field_object]
        current_field_values = [obj.rating for obj in current_field_object]
        current_field = zip(current_field_names, current_field_values)
        current_date = str(date_.today())

        basic_detail={
                    'Name' :candidate_name,
                    'Email':email_id,
                    'Graduation_CGPA':candidate_cgpa,
                    'University_name':candidate_college_name,
                    'interviewer_id':interviewer_id,
                    'feedback_id' : feedback_id,
                    'current_date' : current_date,
                    }

        if(level == 1):
             context = {
                 'basic_detail':basic_detail,
                 'level':level,
                 'form' : form,
                 'req_id' :req_id,
                 'current_field' : current_field,
             }

        if(level == 2):
            feedback_object_1 = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id)
            status = feedback_object_1.status
            comments = feedback_object_1.comments
            interview_date = feedback_object_1.interview_date
            feedback_id_1 = feedback_object_1.pk
            interview_date = feedback_object_1.interview_date
            last_update_time = feedback_object_1.timestamp

            field_object_1 = Field.objects.all().filter(feedback_id = feedback_id_1)
            field_names = [obj.field_name for obj in field_object_1]
            field_values = [obj.rating for obj in field_object_1]
            fields_comments = [obj.comments for obj in field_object_1]
            level_1 = { 'status': status,
                        'comments' : comments,
                        'interviewer_id': interviewer_id,
                        'details' : zip(field_names, field_values, fields_comments),
                        'timestamp' : last_update_time,
                        'feedback_id': feedback_id_1,
                        'interview_date': str(interview_date),
                        'interview_date_show': str(interview_date.strftime('%b. %d, %Y')),
                        }

            context = {
                'basic_detail':basic_detail,
                'level_1': level_1,
                'level':level,
                'form' :form,
                'req_id' :req_id,
                'current_field' : current_field,
            }

        if(level == 3):
            feedback_object_1 = Feedback.objects.get(candidate_email = email_id, level=level-2, requisition_id = req_id)
            status = feedback_object_1.status
            if(status ==  'pass'):
                status = 'selected'
            if(status == 'fail'):
                status = 'rejected'
            comments = feedback_object_1.comments
            interviewer_id = feedback_object_1.interviewer_id
            interview_date = feedback_object_1.interview_date
            feedback_id_1 = feedback_object_1.pk
            last_update_time = feedback_object_1.timestamp

            field_object_1 = Field.objects.all().filter(feedback_id = feedback_id_1)
            field_names = [obj.field_name for obj in field_object_1]
            field_values = [obj.rating for obj in field_object_1]
            fields_comments = [obj.comments for obj in field_object_1]

            feedback_object_2 = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id)
            status_ = feedback_object_2.status
            comments_ = feedback_object_2.comments
            interviewer_id_ = feedback_object_2.interviewer_id
            interview_date_ = feedback_object_2.interview_date
            feedback_id_2 = feedback_object_2.pk
            last_update_time_ = feedback_object_2.timestamp

            field_object_2 = Field.objects.all().filter(feedback_id = feedback_id_2)
            field_names_ = [obj.field_name for obj in field_object_2]
            field_values_ = [obj.rating for obj in field_object_2]
            fields_comments_ = [obj.comments for obj in field_object_2]

            level_1 = { 'status': status,
                        'comments' : comments,
                        'interviewer_id' : interviewer_id,
                        'details' : zip(field_names, field_values, fields_comments),
                        'timestamp' : last_update_time,
                        'feedback_id': feedback_id_1,
                        'interview_date': str(interview_date),
                        'interview_date_show': str(interview_date.strftime('%b. %d, %Y')),
                        }

            level_2 = { 'status': status_,
                        'comments' : comments_,
                        'interviewer_id': interviewer_id_,
                        'details' : zip(field_names_, field_values_, fields_comments_),
                        'timestamp': last_update_time_,
                        'feedback_id' :feedback_id_2,
                        'interview_date' : str(interview_date_),
                        'interview_date_show': str(interview_date_.strftime('%b. %d, %Y')),
                        }

            context = {
                'basic_detail':basic_detail,
                'level_1': level_1,
                'level_2': level_2,
                'level': level,
                'form' :form,
                'req_id' :req_id,
                'current_field' : current_field,
            }

    except Feedback.DoesNotExist:
        raise Http404('Feedback does not exist')

    return render(request, 'registration/feedback.html', context)


def edit(request, req_id, email_id, level, feedback_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        # print(request.method, '======================================================')
        status=request.POST['status']
        # if(status ==  'pass'):
        #     status = 'select'
        # if(status == 'fail'):
        #     status = 'reject'
        # print(status, '+++++++++++++++++++++++++++++++++++++++++++++++++++')
        comments=request.POST['comments']
        interview_date=request.POST['interview_date']
        #
        obj = Feedback.objects.get(feedback_id = feedback_id)
        field_objects = Field.objects.all().filter(feedback_id = obj)

        for field_obj in field_objects:
            field_obj.rating = request.POST[f'rating{field_obj.field_name}{field_obj.pk}']
            field_obj.comments = request.POST[f'comments{field_obj.field_name}{field_obj.pk}']
            field_obj.save()

        obj_ = Feedback.objects.get(pk=feedback_id)
        obj_.status = status
        obj_.comments = comments
        obj_.interview_date = interview_date
        obj_.timestamp = datetime.now()
        obj_.save()

        candidate_email=email_id
        return redirect('../../../../../search_candidate/?candidate_email='+str(candidate_email))
        # return redirect('../../../../../search_candidate/'+str(candidate_email))

    '''GET METHOD'''
    try:
        obj= Feedback.objects.get(pk = feedback_id)
        form = FieldForm(initial={'feedback_id' : obj})
        form.fields['feedback_id'].widget = forms.HiddenInput()

        status = obj.status
        comments = obj.comments
        interview_date = str(obj.interview_date)
        field_object = Field.objects.all().filter(feedback_id = obj)
        field_names= [obj_.field_name for obj_ in field_object]
        field_values= [obj_.rating for obj_ in field_object]
        field_comments = [obj_.comments for obj_ in field_object]
        field_id = [obj_.field_id for obj_ in field_object]
        level_ = obj.level
        current_date = str(date_.today())

        interview_date_1 = Feedback.objects.get(candidate_email = email_id, level=1, requisition_id = req_id).interview_date
        interview_date_2 = Feedback.objects.get(candidate_email = email_id, level=2, requisition_id = req_id).interview_date
        Context = {
            'status': status,
            'comments': comments,
            'fields': zip(field_names, field_values, field_comments, field_id),
            'level' : level_,
            'feedback_id': feedback_id,
            'form': form,
            'interview_date': interview_date,
            'email_id':email_id,
            'current_date':current_date,
            'interview_date_1':str(interview_date_1),
            'interview_date_2':str(interview_date_2),
        }
        return render(request, 'registration/edit.html', Context)
    except:
        return HttpResponse('No details Found')

def field_view(request, req_id, email_id, level, feedback_id):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")

    level_ = Feedback.objects.get(feedback_id=feedback_id).level
    if request.method == 'POST':
        form = FieldForm(request.POST)
        if form.is_valid():
            field_name = form.cleaned_data['field_name']
            print(field_name)
            form.save()

        if(level == level_):
            return redirect('../../#field')
        return redirect(f'../../edit{feedback_id}/')

def delete_field(request, req_id, email_id, level, field_name, del_level):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")
    feedback_id = Feedback.objects.get(candidate_email=email_id, requisition_id=req_id, level =del_level).pk
    obj = Field.objects.get(feedback_id = feedback_id, field_name = field_name)
    obj.delete()
    if(level == del_level):
        return redirect('../')
    return redirect(f'../edit{feedback_id}')


def download_report(request, req_id, email_id, level):
    # print(os.getcwd())
    pdfkit.from_file('Incedoinc/templates/registration/report.html', f'media/feedbacks/{req_id}{email_id}.pdf')
    return redirect('../report/')


def test(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")

    return HttpResponse('inside the test')


def report_view(request, req_id, email_id, level):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")

    candidate_object = Candidate.objects.get(email=email_id)
    candidate_name = candidate_object.full_name
    candidate_email = candidate_object.email
    candidate_college = candidate_object.college_name
    candidate_cgpa = candidate_object.CGPA

    basic_detail = {
        'candidate_name':candidate_name,
        'candidate_email':candidate_email,
        'candidate_college':candidate_college,
        'candidate_cgpa':candidate_cgpa,
    }

    feedback_object_1 = Feedback.objects.get(candidate_email = email_id, level=1, requisition_id = req_id)
    status = feedback_object_1.status
    comments = feedback_object_1.comments
    interviewer_id = feedback_object_1.interviewer_id
    feedback_id_1 = feedback_object_1.pk
    last_update_time = feedback_object_1.timestamp
    interview_date = feedback_object_1.interview_date

    field_object_1 = Field.objects.all().filter(feedback_id = feedback_id_1)
    field_names = [obj.field_name for obj in field_object_1]
    field_values = [obj.rating for obj in field_object_1]
    fields_comments = [obj.comments for obj in field_object_1]
    level_1 = { 'status': status,
                'comments' : comments,
                'interviewer_id': interviewer_id,
                'details' : zip(field_names, field_values, fields_comments),
                'timestamp' : last_update_time,
                'feedback_id': feedback_id_1,
                'interview_date' : interview_date,
    }

    feedback_object_2 = Feedback.objects.get(candidate_email = email_id, level=2, requisition_id = req_id)
    status = feedback_object_2.status
    comments = feedback_object_2.comments
    interviewer_id = feedback_object_2.interviewer_id
    feedback_id_2 = feedback_object_2.pk
    last_update_time = feedback_object_2.timestamp
    interview_date = feedback_object_2.interview_date

    field_object_2 = Field.objects.all().filter(feedback_id = feedback_id_2)
    field_names = [obj.field_name for obj in field_object_2]
    field_values = [obj.rating for obj in field_object_2]
    fields_comments = [obj.comments for obj in field_object_2]
    level_2 = { 'status': status,
                'comments' : comments,
                'interviewer_id': interviewer_id,
                'details' : zip(field_names, field_values, fields_comments),
                'timestamp' : last_update_time,
                'feedback_id': feedback_id_1,
                'interview_date' : interview_date,
                }

    feedback_object_3 = Feedback.objects.get(candidate_email = email_id, level=3, requisition_id = req_id)
    status = feedback_object_3.status
    comments = feedback_object_3.comments
    interviewer_id = feedback_object_3.interviewer_id
    feedback_id_3 = feedback_object_3.pk
    last_update_time = feedback_object_3.timestamp
    interview_date = feedback_object_3.interview_date

    field_object_3 = Field.objects.all().filter(feedback_id = feedback_id_3)
    field_names = [obj.field_name for obj in field_object_3]
    field_values = [obj.rating for obj in field_object_3]
    fields_comments = [obj.comments for obj in field_object_3]
    level_3 = { 'status': status,
                'comments' : comments,
                'interviewer_id': interviewer_id,
                'details' : zip(field_names, field_values, fields_comments),
                'timestamp' : last_update_time,
                'feedback_id': feedback_id_1,
                'interview_date': interview_date,
                }

    context = {
        'basic_detail':basic_detail,
        'level_1':level_1,
        'level_2':level_2,
        'level_3':level_3,
    }

    return render(request, 'registration/report.html', context)


def referrals_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        print(type(request.POST))
        print(request.POST)
        if 'home_button' in request.POST:
             return redirect('home_page')
        elif 'refer_candidate' in request.POST:
            return redirect('../referrals/refer_candidate/%s' %request.POST['refer_candidate'])
        elif 'my_referrals' in request.POST:
            return redirect('../referrals/my_referrals/%s' %Employee.objects.get(email=request.user.username).employee_id)
        elif 'listallopen' in request.POST:
            open_to_internal_list=['yes','no']
            if 'open_to_internal' in request.POST:
                open_to_internal_list=request.POST.getlist('open_to_internal')
            requisition_status_list=['open','onhold']
            if 'requisition_status' in request.POST:
                requisition_status_list=request.POST.getlist('requisition_status')
            temp_list_tuple = list(set(Job.objects.filter(open_to_internal__in=open_to_internal_list ,requisition_status__in=requisition_status_list)))
            if len(temp_list_tuple)==0:
                return render(request, 'referrals.html',{'error_message':'Oops :( So Empty'})
            context={}
            for x in range(len(temp_list_tuple)):
                context[x+1]=temp_list_tuple[x]
            # print(context,"asdfdsfsdfsdfsd")
            return render(request, 'referrals.html',{'context':context})
        elif 'search' in request.POST:
            search_element=request.POST['search_element']

            if(len(search_element)==0):
                return render(request, 'referrals.html',{'error_message':'Please Enter Something'})
            # print(search_element,"-----------------")
            open_to_internal_list=['yes','no']
            if 'open_to_internal' in request.POST:
                open_to_internal_list=request.POST.getlist('open_to_internal')
            requisition_status_list=['open','onhold']
            if 'requisition_status' in request.POST:
                requisition_status_list=request.POST.getlist('requisition_status')
            temp_list_tuple = list(set(Job.objects.filter(Q(requisition_id__contains=search_element , open_to_internal__in=open_to_internal_list ,requisition_status__in=requisition_status_list) | Q(jd__in=JD.objects.filter(jd_name__contains=search_element) , open_to_internal__in=open_to_internal_list ,requisition_status__in=requisition_status_list))))
            print(open_to_internal_list)
            print(len(temp_list_tuple))
            if len(temp_list_tuple)==0:
                return render(request, 'referrals.html',{'error_message':'No Matching results'})
            context={}
            for x in range(len(temp_list_tuple)):
                context[x+1]=temp_list_tuple[x]
            # print(context,"asdfdsfsdfsdfsd")
            return render(request, 'referrals.html',{'context':context})


    return render(request, 'referrals.html')

def my_referrals_view(request,employee_id):
    if not request.user.is_authenticated:
        return redirect('login')
    if 'home_button' in request.POST:
        return redirect('home_page')
    if 'go_back' in request.POST:
            return redirect('referrals_page')
    temp_list_tuple = list(set(RequisitionCandidate.objects.filter(referred_by=Employee.objects.get(employee_id=employee_id))))
    if len(temp_list_tuple)==0:
        return render(request, 'my_referrals.html',{'error_message':'Something Went Wrong'})
    context={}
    for x in range(len(temp_list_tuple)):
        context[x+1]=temp_list_tuple[x]
    # print(context,"asdfdsfsdfsdfsd")
    return render(request, 'my_referrals.html',{'context':context})

    print(employee_id,"{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}")


def refer_candidate_view(request,requisition_id):
    if not request.user.is_authenticated:
        return redirect('login')
    if 'home_button' in request.POST:
        return redirect('home_page')
    if 'go_back' in request.POST:
            return redirect('referrals_page')
    job_obj=Job.objects.filter(requisition_id=requisition_id)
    # print(type(job_obj[0]))
    if(len(job_obj)==0):
        return render(request, 'refer_candidate.html',{'error_message':'Oops , Something went wrong!'})
    context={}
    requisition_candidate_obj_dict={}
    if request.method=='POST':
        print(request.POST)
        if 'yes' in request.POST:
            candidate_obj=Candidate.objects.filter(email=request.POST['yes'])[0]
            RequisitionCandidate.objects.create(
                requisition_id=job_obj[0],
                candidate_email=candidate_obj,
                referred_by=Employee.objects.get(email=request.user.username),
                candidate_status='in_progress',
                referred_date=date_.today()
            )

            Feedback.objects.create(
                candidate_email=candidate_obj,
                level=1,
                requisition_id=job_obj[0],
                status='pending',
            )
            Feedback.objects.create(
                candidate_email=candidate_obj,
                level=2,
                requisition_id=job_obj[0],
                status='pending',
            )
            Feedback.objects.create(
                candidate_email=candidate_obj,
                level=3,
                requisition_id=job_obj[0],
                status='pending',
            )
            ########Vaishnavi###########
            
            mail_subject = 'New Candidate Referred'
            message = render_to_string('new_candidate_referred.html', {
                'req_id': job_obj[0],
                'candidate_email': candidate_obj,
                'referred_by':Employee.objects.get(email=request.user.username),
                
                
            })
            to_email = "vaishnavi.s@incedoinc.com"
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            file_url = candidate_obj.resume.url
            full_path = os.path.join(settings.BASE_DIR, file_url[1:])
            file = open(full_path, 'rb')

            email.attach(candidate_obj.get_resume_name(), file.read(), 'application/pdf/')
            email.send()
     ##############   To Candidate #######################
            mail_subject = 'Successfully Applied'
            message = render_to_string('successfully_applied.html', {
                'req_id': job_obj[0],
                # 'candidate_email': candidate_obj,
                'referred_by':Employee.objects.get(email=request.user.username),
                
                
            })
            to_email = candidate_obj.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            # print("asdasdsa")
        if 'refer_this_candidate' in request.POST:
            confirmation_candidate_obj=(Candidate.objects.filter(email=request.POST['refer_this_candidate']))[0]
            print("asdasdasd-----",type(confirmation_candidate_obj))
            return render(request, 'refer_candidate.html',{'job_obj':job_obj[0],'confirmation_candidate_obj':confirmation_candidate_obj})
        if 'search' in request.POST:
            if len(request.POST['search_element'])==0:
                return render(request, 'refer_candidate.html',{'job_obj':job_obj[0],'error_message_2':'Please Enter Something'})
            candidate_obj=Candidate.objects.filter(Q(f_name__contains=request.POST['search_element']) | Q(email__contains=request.POST['search_element']))
            if(len(candidate_obj)==0):
                return render(request, 'refer_candidate.html',{'job_obj':job_obj[0],'error_message_2':'No Matching results'})
            for x in range(len(candidate_obj)):
                temp_dict={}
                temp_dict['candidate_obj']=candidate_obj[x]
                requisition_candidate_obj=RequisitionCandidate.objects.filter(requisition_id=job_obj[0],candidate_email=candidate_obj[x])
                if len(requisition_candidate_obj)==0:
                    temp_dict['requisition_candidate_obj']=None
                else:
                    temp_dict['requisition_candidate_obj']=requisition_candidate_obj[0]
                context[x+1]=temp_dict

            print("context[[[[[[]]]]]]",context)



    return render(request, 'refer_candidate.html',{'job_obj':job_obj[0],'context':context,'requisition_candidate_obj_dict':requisition_candidate_obj_dict})
