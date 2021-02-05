from django.core.exceptions import ValidationError
from django.db.models import query
from django.shortcuts import redirect, render
from decimal import Context
from django.contrib.auth.backends import UserModel
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from datetime import datetime

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


#

# Vaishnavi changed authentication

#include models
from .models import Employee, JD, Job, Candidate, Feedback
from .models import TestModel

#include forms
from .forms import CandidateForm, UploadJdForm, UploadJobForm
from .forms import TestForm

#for downloading file
# import os
# from django.conf import settings
# from django.http import HttpResponse, Http404
# def download_view(request, path):
#     print('path: ', path)
#     file_path = os.path.join(settings.MEDIA_ROOT, path)
#     print('file_path: ', file_path)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#             response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#             return response
#     raise Http404
################################################################################

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return HttpResponseRedirect(reverse('first_page'))

def manage_jd_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')

    user = Employee.objects.get(email=request.user.username)
    print(user)
    if request.method == 'POST':
        if 'search_button' in request.POST:
            search_query = request.POST['search_query']
            query_set = JD.objects.filter(jd_name__contains=search_query)
            context = {
                'query_set': query_set
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

    if request.method == 'POST':
        if 'search_button' in request.POST:
            search_query = request.POST['search_query']
            query_set = Job.objects.filter(requisition_id__contains=search_query)
            context = {
                'query_set': query_set
            }
            return render(request, 'manage_job.html', context)
        elif 'list_all_button' in request.POST:
            query_set = Job.objects.all()
            context = {
                'query_set': query_set
            }
            return render(request, 'manage_job.html', context)
        elif 'raise_requisition_button' in request.POST:
            return redirect('upload_job_page')
        elif 'delete_job_button' in request.POST:
            return HttpResponse('<h1>delete job</h1>')

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
            # print(form.cleaned_data)
            obj = form.save()
            return redirect('manage_jd_page')
    else:
        form = UploadJdForm(initial={'uploaded_by_employee':user})
        form.fields['uploaded_by_employee'].disabled = True
    context = {
        'form' : form
    }
    return render(request, 'upload_jd.html', context)


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
            # print(form.cleaned_data)
            obj = form.save()
            return redirect('manage_job_page')
    else:
        form = UploadJobForm(initial={'raised_by_employee':user})
        form.fields['raised_by_employee'].disabled = True
    context = {
        'form' : form
    }
    return render(request, 'upload_job.html', context)


def home_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        # print(request.POST)
        if 'search_requisition_id_button' in request.POST:
            requisition_id = request.POST.get('requisition_id')
            if len(requisition_id) >= 3:
                query_set = Job.objects.filter(requisition_id__contains=requisition_id)
            else:
                query_set = Job.objects.filter(requisition_id=requisition_id)
            # print(query_set)
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
        else:
            return Http404('Page Not Exist')
    return render(request,'home.html')

# def search_jd_view(request, requisition_id):
#     if not request.user.is_authenticated:
#         return redirect('login')
#     obj = Job.objects.get(requisition_id=requisition_id)
#     if obj is not None:
#         context = {
#             'obj': obj
#         }
#         return render(request, 'jd_results.html', context)
#     else:
#         raise Http404("JD is not exist")

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
            return redirect('../'+'search_candidate'+'/'+str(candidate_email))
    else:
        form = CandidateForm(initial={'registered_by': user})
        form.fields['registered_by'].disabled = True
    context = {
        'form': form
    }
    return render(request, 'add_candidate.html', context)
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
    if request.method == 'POST':
        candidate_obj=Candidate.objects.get(email=candidate_email)
        print(candidate_obj)
        print("----------------------")
        print(type(request.POST)," : ",request.POST)
        print("----------------------")
        print(type(request.POST['fname'])," : ",request.POST['fname'])
        print(type(request.POST['lname'])," : ",request.POST['lname'])
        print(type(request.POST['mname'])," : ",request.POST['mname'])
        print(type(request.POST['gender'])," : ",request.POST['gender'])
        print(type(request.POST['CGPA'])," : ",request.POST['CGPA'])
        print(type(request.POST['college'])," : ",request.POST['college'])
        print(type(request.POST['experience'])," : ",request.POST['experience'])
        print(type(request.POST['mobile_no'])," : ",request.POST['mobile_no'])
        print(type(request.POST['DOB'])," : ",request.POST['DOB'])
        print(type(request.POST['project'])," : ",request.POST['project'])
        print(type(request.POST['noticePeriod'])," : ",request.POST['noticePeriod'])
        print(type(request.POST['resume'])," : ",request.POST['resume'])
        if len(request.POST['fname'])!=0 :
            candidate_obj.f_name=request.POST['fname']
        if len(request.POST['mname'])!=0 :
            candidate_obj.m_name=request.POST['mname']
        if len(request.POST['lname'])!=0 :
            candidate_obj.l_name=request.POST['lname']
        if len(request.POST['gender'])!=0 :
            candidate_obj.gender=request.POST['gender']
        if len(request.POST['CGPA'])!=0 :
            candidate_obj.CGPA=request.POST['CGPA']
        if len(request.POST['college'])!=0 :
            candidate_obj.college_name=request.POST['college']
        if len(request.POST['experience'])!=0 :
            candidate_obj.experience=request.POST['experience']
        if len(request.POST['mobile_no'])!=0 :
            candidate_obj.mobile=request.POST['mobile_no']
        if len(request.POST['DOB'])!=0 :
            candidate_obj.DOB=request.POST['DOB']
        if len(request.POST['project'])!=0 :
            candidate_obj.projects_link=request.POST['project']
        if len(request.POST['noticePeriod'])!=0 :
            candidate_obj.noticePeriod=request.POST['noticePeriod']
        candidate_obj.save()
        print(candidate_obj.email)
        return redirect('../view_candidate/'+str(candidate_email))
    candidate_obj=Candidate.objects.filter(email=candidate_email)
    print(candidate_obj[0].email)
    return render(request,'edit_candidate.html',{'candidate_obj':candidate_obj[0]})

def view_candidate(request,candidate_email):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        candidate_obj=Candidate.objects.filter(email=candidate_email)
        print(candidate_email)

        print("sdfsdfsdfsd------------------------------")
        return redirect('../edit_candidate/'+str(candidate_email))
    candidate_obj=Candidate.objects.filter(email=candidate_email)
    # print(candidate_obj[0].email)
    return render(request,'view_candidate.html',{'candidate_obj':candidate_obj[0]})

def search_candidate(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'GET' and kwargs:
            if not kwargs['candidate_email']:
                raise ValidationError('Get request has arguments type which are not supported')
            candidate_email = kwargs['candidate_email']
            if len(candidate_email)==0:
                return render(request, 'search.html',{'error_message':'Please enter something'})
            candidate_list = list(Candidate.objects.filter(email__contains=candidate_email))
            if len(candidate_list)==0 :
                return render(request, 'search.html',{'error_message':'No matching Candidate for \''+str(candidate_email)+'\''})
            result=[]
            for c in candidate_list:
                print(c.email)
                temp_req_id_list = list(set(Feedback.objects.filter(candidate_email=c).values_list('requisition_id').order_by('-requisition_id')))
                for r in temp_req_id_list:
                    result.append([r[0],c.email])
            print (result)
            if len(result)==0 :
                return render(request, 'search.html',{'error_message':'No matching results'})
            context = {}
            for x in range(len(result)):
                temp_dict={}
                # print(type(candidate_list[x][0]))
                l1=Feedback.objects.get(requisition_id=result[x][0],candidate_email=result[x][1], level = 1).status
                temp_dict['req_id']=result[x][0];
                temp_dict['email']=result[x][1];
                temp_dict['resume'] = Candidate.objects.get(email=result[x][1]).resume
                if l1=='pending':
                    temp_dict[1]='pending'
                    temp_dict[2]='-'
                    temp_dict[3]='-'
                elif l1=='fail':
                    temp_dict[1]='fail'
                    temp_dict[2]='NA'
                    temp_dict[3]='NA'
                else :
                    l2=Feedback.objects.get(requisition_id=result[x][0],candidate_email=result[x][1], level = 2).status
                    if l2=='pending':
                        temp_dict[1]='pass'
                        temp_dict[2]='pending'
                        temp_dict[3]='-'
                    elif l1=='fail':
                        temp_dict[1]='pass'
                        temp_dict[2]='fail'
                        temp_dict[3]='NA'
                    else :
                        l3=Feedback.objects.get(requisition_id=result[x][0],candidate_email=result[x][1], level = 3).status
                        if l3=='pending':
                            temp_dict[1]='pass'
                            temp_dict[2]='pass'
                            temp_dict[3]='pending'
                        elif l3=='fail':
                            temp_dict[1]='pass'
                            temp_dict[2]='pass'
                            temp_dict[3]='fail'
                        else:
                            temp_dict[1]='pass'
                            temp_dict[2]='pass'
                            temp_dict[3]='pass'
                context[str(x+1)]=temp_dict
            return render(request, 'search.html',{'context':context})
    elif request.method == 'POST':
        if request.POST['dropdown'] == 'req_id':
            requisition_id=request.POST['search_element']
            if len(requisition_id)==0:
                return render(request, 'search.html',{'error_message':'Please enter something'})
            req_id_list=list(Job.objects.filter(requisition_id__contains=requisition_id))
            print(req_id_list,"------------------------------")
            if len(req_id_list)==0 :
                 return render(request, 'search.html',{'error_message':'No matching Requition Id for \''+str(requisition_id)+'\''})
            result=[]
            for r in req_id_list:
                print(r.requisition_id)
                temp_candidate_list = list(set(Feedback.objects.filter(requisition_id=r).values_list('candidate_email').order_by('-candidate_email')))
                for c in temp_candidate_list:
                    # print (c[0])
                    # print("{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}")
                    result.append([r.requisition_id,c[0]])
                    # print(result)
                    # print("..................")
                print(result)
            if len(result)==0 :
                return render(request, 'search.html',{'error_message':'No candidate(s) applied for Requitio Id matching \''+str(requisition_id+'\'')})
            context = {}
            for x in range(len(result)):
                temp_dict={}
                # print(type(candidate_list[x][0]))
                l1=Feedback.objects.get(requisition_id=result[x][0],candidate_email=result[x][1], level = 1).status
                temp_dict['req_id']=result[x][0];
                temp_dict['email']=result[x][1];
                temp_dict['resume'] = Candidate.objects.get(email=result[x][1]).resume
                if l1=='pending':
                    temp_dict[1]='pending'
                    temp_dict[2]='-'
                    temp_dict[3]='-'
                elif l1=='fail':
                    temp_dict[1]='fail'
                    temp_dict[2]='NA'
                    temp_dict[3]='NA'
                else :
                    l2=Feedback.objects.get(requisition_id=result[x][0],candidate_email=result[x][1], level = 2).status
                    if l2=='pending':
                        temp_dict[1]='pass'
                        temp_dict[2]='pending'
                        temp_dict[3]='-'
                    elif l1=='fail':
                        temp_dict[1]='pass'
                        temp_dict[2]='fail'
                        temp_dict[3]='NA'
                    else :
                        l3=Feedback.objects.get(requisition_id=result[x][0],candidate_email=result[x][1], level = 3).status
                        if l3=='pending':
                            temp_dict[1]='pass'
                            temp_dict[2]='pass'
                            temp_dict[3]='pending'
                        elif l3=='fail':
                            temp_dict[1]='pass'
                            temp_dict[2]='pass'
                            temp_dict[3]='fail'
                        else:
                            temp_dict[1]='pass'
                            temp_dict[2]='pass'
                            temp_dict[3]='pass'
                context[str(x+1)]=temp_dict
                # print("candidate:list",candidate_list)
            print(request.POST['dropdown'])
                # print(requisition_id)
            return render(request, 'search.html',{'context':context})
        else :
            candidate_email= request.POST['search_element']
            if len(candidate_email)==0:
                return render(request, 'search.html',{'error_message':'Please enter something'})
            candidate_list = list(Candidate.objects.filter(email__contains=candidate_email))
            if len(candidate_list)==0 :
                return render(request, 'search.html',{'error_message':'No matching Candidate for \''+str(candidate_email)+'\''})
            result=[]
            for c in candidate_list:
                print(c.email)
                temp_req_id_list = list(set(Feedback.objects.filter(candidate_email=c).values_list('requisition_id').order_by('-requisition_id')))
                for r in temp_req_id_list:
                    result.append([r[0],c.email])
            print (result)
            if len(result)==0 :
                return render(request, 'search.html',{'error_message':'No matching results'})
            context = {}
            for x in range(len(result)):
                temp_dict={}
                # print(type(candidate_list[x][0]))
                l1=Feedback.objects.get(requisition_id=result[x][0],candidate_email=result[x][1], level = 1).status
                temp_dict['req_id']=result[x][0];
                temp_dict['email']=result[x][1];
                temp_dict['resume'] = Candidate.objects.get(email=result[x][1]).resume
                if l1=='pending':
                    temp_dict[1]='pending'
                    temp_dict[2]='-'
                    temp_dict[3]='-'
                elif l1=='fail':
                    temp_dict[1]='fail'
                    temp_dict[2]='NA'
                    temp_dict[3]='NA'
                else :
                    l2=Feedback.objects.get(requisition_id=result[x][0],candidate_email=result[x][1], level = 2).status
                    if l2=='pending':
                        temp_dict[1]='pass'
                        temp_dict[2]='pending'
                        temp_dict[3]='-'
                    elif l1=='fail':
                        temp_dict[1]='pass'
                        temp_dict[2]='fail'
                        temp_dict[3]='NA'
                    else :
                        l3=Feedback.objects.get(requisition_id=result[x][0],candidate_email=result[x][1], level = 3).status
                        if l3=='pending':
                            temp_dict[1]='pass'
                            temp_dict[2]='pass'
                            temp_dict[3]='pending'
                        elif l3=='fail':
                            temp_dict[1]='pass'
                            temp_dict[2]='pass'
                            temp_dict[3]='fail'
                        else:
                            temp_dict[1]='pass'
                            temp_dict[2]='pass'
                            temp_dict[3]='pass'
                context[str(x+1)]=temp_dict
        return render(request, 'search.html',{'context':context})
    else:
        return render(request, 'search.html')


def feedback(request, req_id, email_id, level):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        status = request.POST['status']
        rating_python = request.POST['rating_python']
        rating_java = request.POST['rating_java']
        rating_cpp = request.POST['rating_cpp']
        rating_sql = request.POST['rating_sql']
        comments = request.POST['comments']
        interviewer_id = Employee.objects.get(email=request.user._wrapped.username).employee_id

        feedback_object = Feedback.objects.get(candidate_email=Candidate.objects.get(email=email_id), requisition_id=Job.objects.get(requisition_id = req_id), level=level, status='pending')
        # feedback_object.interviewer_id = Employee.objects.get(employee_id=interviewer_code)
        feedback_object.status=status
        feedback_object.rating_python=rating_python
        feedback_object.rating_java=rating_java
        feedback_object.rating_cpp=rating_cpp
        feedback_object.rating_sql=rating_sql
        feedback_object.comments=comments
        feedback_object.interviewer_id = Employee.objects.get(employee_id=interviewer_id)
        feedback_object.save()

        candidate_email=email_id
        return redirect('../../../../search_candidate/'+str(candidate_email))

    '''GET part'''
    try:
        candidate_name = Candidate.objects.get(email=email_id).full_name
        candidate_cgpa = Candidate.objects.get(email=email_id).CGPA
        candidate_college_name =  Candidate.objects.get(email=email_id).college_name
        interviewer_id = Employee.objects.get(email=request.user._wrapped.username)
        basic_detail={'Name' :candidate_name,
                    'Email':email_id,
                    'Graduation_CGPA':candidate_cgpa,
                    'University_name':candidate_college_name,
                    'interviewer_id':interviewer_id,
                    }

        if(level == 1):
             context = {
                 'basic_detail':basic_detail,
                 'level':level
             }

        if(level == 2):
            status = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).status
            python_rating = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).rating_python
            java_rating = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).rating_java
            cpp_rating = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).rating_cpp
            sql_rating = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).rating_sql
            comments = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).comments
            interviewer_id = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).interviewer_id

            level_1 = { 'status': status,
                        'python_rating': python_rating,
                        'java_rating': java_rating,
                        'cpp_rating': cpp_rating,
                        'sql_rating': sql_rating,
                        'comments' : comments,
                        'interviewer_id': interviewer_id,
                        }

            context = {
                'basic_detail':basic_detail,
                'level_1': level_1,
                'level':level
            }

        if(level == 3):
            status = Feedback.objects.get(candidate_email = email_id, level=level-2, requisition_id = req_id).status
            python_rating = Feedback.objects.get(candidate_email = email_id, level=level-2, requisition_id = req_id).rating_python
            java_rating = Feedback.objects.get(candidate_email = email_id, level=level-2, requisition_id = req_id).rating_java
            cpp_rating = Feedback.objects.get(candidate_email = email_id, level=level-2, requisition_id = req_id).rating_cpp
            sql_rating = Feedback.objects.get(candidate_email = email_id, level=level-2, requisition_id = req_id).rating_sql
            comments = Feedback.objects.get(candidate_email = email_id, level=level-2, requisition_id = req_id).comments
            interviewer_id = Feedback.objects.get(candidate_email = email_id, level=level-2, requisition_id = req_id).interviewer_id

            status_ = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).status
            python_rating_ = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).rating_python
            java_rating_ = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).rating_java
            cpp_rating_ = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).rating_cpp
            sql_rating_ = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).rating_sql
            comments_ = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).comments
            interviewer_id_ = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).interviewer_id

            level_1 = { 'status': status,
                        'python_rating': python_rating,
                        'java_rating': java_rating,
                        'cpp_rating': cpp_rating,
                        'sql_rating': sql_rating,
                        'comments' : comments,
                        'interviewer_id' : interviewer_id,
                        }

            level_2 = { 'status': status_,
                        'python_rating': python_rating_,
                        'java_rating': java_rating_,
                        'cpp_rating': cpp_rating_,
                        'sql_rating': sql_rating_,
                        'comments' : comments_,
                        'interviewer_id': interviewer_id_,
                        }

            context = {
                'basic_detail':basic_detail,
                'level_1': level_1,
                'level_2': level_2,
                'level': level,
            }

    except Feedback.DoesNotExist:
        raise Http404('Feedback does not exist')

    return render(request, 'registration/feedback.html', context)

def edit(request, req_id, email_id, level, edit_level):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        status=request.POST['status']
        rating_python=request.POST['rating_python']
        rating_java=request.POST['rating_java']
        rating_cpp=request.POST['rating_cpp']
        rating_sql=request.POST['rating_sql']
        comments=request.POST['comments']

        obj_ = Feedback.objects.get(candidate_email=email_id, requisition_id=req_id, level=edit_level)
        obj_.status = status
        obj_.rating_python = rating_python
        obj_.rating_java = rating_java
        obj_.rating_cpp = rating_cpp
        obj_.rating_sql = rating_sql
        obj_.comments = comments
        obj_.save()

        candidate_email=email_id
        return redirect('../../../../../search_candidate/'+str(candidate_email))


    try:
        obj= Feedback.objects.get(candidate_email=email_id, requisition_id=req_id, level=edit_level)
        Context = vars(obj)
        return render(request, 'registration/edit.html', Context)
    except:
        return HttpResponse('No details Found')


def test(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")

    return HttpResponse('inside the test')




# def search_candidate_original(request, *args, **kwargs):
#     if not request.user.is_authenticated:
#         return redirect('login')
#
#     if request.method == 'POST' or kwargs:
#         if request.method == 'GET' and kwargs:
#             if not kwargs['candidate_email']:
#                 raise ValidationError('Get request has arguments type which are not supported')
#             candidate_email = kwargs['candidate_email']
#         elif request.method == 'POST':
#             if request.POST['dropdown'] == 'req_id':
#                 requisition_id=request.POST['search_element']
#                 candidate_list = list(set(Feedback.objects.filter(requisition_id=requisition_id).values_list('candidate_email').order_by('-candidate_email')))
#                 if len(candidate_list)==0 :
#                     return render(request, 'search.html',{'error_message':'There are no results for this Requisition Id'})
#                 context = {}
#                 for x in range(len(candidate_list)):
#                     temp_dict={}
#                     print(type(candidate_list[x][0]))
#                     l1=Feedback.objects.get(requisition_id=requisition_id,candidate_email=candidate_list[x][0], level = 1).status
#
#                     temp_dict['req_id']=requisition_id;
#                     temp_dict['email']=candidate_list[x][0];
#                     temp_dict['resume'] = Candidate.objects.get(email=candidate_list[x][0]).resume
#                     if l1=='pending':
#                         temp_dict[1]='pending'
#                         temp_dict[2]='-'
#                         temp_dict[3]='-'
#                     elif l1=='fail':
#                         temp_dict[1]='fail'
#                         temp_dict[2]='NA'
#                         temp_dict[3]='NA'
#                     else :
#                         l2=Feedback.objects.get(requisition_id=requisition_id,candidate_email=candidate_list[x][0], level = 2).status
#                         if l2=='pending':
#                             temp_dict[1]='pass'
#                             temp_dict[2]='pending'
#                             temp_dict[3]='-'
#                         elif l1=='fail':
#                             temp_dict[1]='pass'
#                             temp_dict[2]='fail'
#                             temp_dict[3]='NA'
#                         else :
#                             l3=Feedback.objects.get(requisition_id=requisition_id,candidate_email=candidate_list[x][0], level = 3).status
#                             if l3=='pending':
#                                 temp_dict[1]='pass'
#                                 temp_dict[2]='pass'
#                                 temp_dict[3]='pending'
#                             elif l3=='fail':
#                                 temp_dict[1]='pass'
#                                 temp_dict[2]='pass'
#                                 temp_dict[3]='fail'
#                             else:
#                                 temp_dict[1]='pass'
#                                 temp_dict[2]='pass'
#                                 temp_dict[3]='pass'
#                     context[str(x+1)]=temp_dict
#
#                 print("candidate:list",candidate_list)
#                 print(request.POST['dropdown'])
#                 print(requisition_id)
#                 return render(request, 'search.html',{'context':context})
#             else :
#                 candidate_email= request.POST['search_element']
#                 req_id_list = list(set(Feedback.objects.filter(candidate_email = candidate_email).values_list('requisition_id').order_by('-requisition_id')))
#                 if len(req_id_list)==0 :
#                     return render(request, 'search.html',{'error_message':'There are no results for this Candidate'})
#                 context = {}
#                 for x in range(len(req_id_list)):
#                     temp_dict={}
#                     print(type(req_id_list[x][x][0]))
#                     l1=Feedback.objects.get(requisition_id=req_id_list[x][0],candidate_email=candidate_email, level = 1).status
#
#                     temp_dict['req_id']=req_id_list[x][0];
#                     temp_dict['email']=candidate_email;
#                     temp_dict['resume'] = Candidate.objects.get(email=candidate_email).resume
#                     if l1=='pending':
#                         temp_dict[1]='pending'
#                         temp_dict[2]='-'
#                         temp_dict[3]='-'
#                     elif l1=='fail':
#                         temp_dict[1]='fail'
#                         temp_dict[2]='NA'
#                         temp_dict[3]='NA'
#                     else :
#                         l2=Feedback.objects.get(requisition_id=req_id_list[x][0],candidate_email=candidate_email, level = 2).status
#                         if l2=='pending':
#                             temp_dict[1]='pass'
#                             temp_dict[2]='pending'
#                             temp_dict[3]='-'
#                         elif l1=='fail':
#                             temp_dict[1]='pass'
#                             temp_dict[2]='fail'
#                             temp_dict[3]='NA'
#                         else :
#                             l3=Feedback.objects.get(requisition_id=req_id_list[x][0],candidate_email=candidate_email, level = 3).status
#                             if l3=='pending':
#                                 temp_dict[1]='pass'
#                                 temp_dict[2]='pass'
#                                 temp_dict[3]='pending'
#                             elif l3=='fail':
#                                 temp_dict[1]='pass'
#                                 temp_dict[2]='pass'
#                                 temp_dict[3]='fail'
#                             else:
#                                 temp_dict[1]='pass'
#                                 temp_dict[2]='pass'
#                                 temp_dict[3]='pass'
#                     context[str(x+1)]=temp_dict
#
#                 print("req list",req_id_list)
#                 print(request.POST['dropdown'])
#                 print(candidate_email)
#
#                 return render(request, 'search.html',{'context':context})
#         # req_id = list(set(Feedback.objects.filter(candidate_email = candidate_email).values_list('requisition_id').order_by('-requisition_id')))
#         # if len(req_id)==0 :
#         #     return render(request, 'search.html',{'error_message':'There are no results for this input'})
#         #
#         # print(type(req_id))
#         # print(req_id)
#         # print("asfaddfsdfs",request.POST['dropdown'])
#         # context = {}
#         # for x in range(len(req_id)):
#         #     temp_dict={}
#         #     print(type(req_id[x][0]))
#         #     l1=Feedback.objects.get(requisition_id=req_id[x][0],candidate_email=candidate_email, level = 1).status
#         #
#         #     temp_dict['req_id']=req_id[x][0];
#         #     temp_dict['email']=candidate_email;
#         #     temp_dict['resume'] = Candidate.objects.get(email=candidate_email).resume
#         #     if l1=='pending':
#         #         temp_dict[1]='pending'
#         #         temp_dict[2]='-'
#         #         temp_dict[3]='-'
#         #     elif l1=='fail':
#         #         temp_dict[1]='fail'
#         #         temp_dict[2]='NA'
#         #         temp_dict[3]='NA'
#         #     else :
#         #         l2=Feedback.objects.get(requisition_id=req_id[x][0],candidate_email=candidate_email, level = 2).status
#         #         if l2=='pending':
#         #             temp_dict[1]='pass'
#         #             temp_dict[2]='pending'
#         #             temp_dict[3]='-'
#         #         elif l1=='fail':
#         #             temp_dict[1]='pass'
#         #             temp_dict[2]='fail'
#         #             temp_dict[3]='NA'
#         #         else :
#         #             l3=Feedback.objects.get(requisition_id=req_id[x][0],candidate_email=candidate_email, level = 3).status
#         #             if l3=='pending':
#         #                 temp_dict[1]='pass'
#         #                 temp_dict[2]='pass'
#         #                 temp_dict[3]='pending'
#         #             elif l3=='fail':
#         #                 temp_dict[1]='pass'
#         #                 temp_dict[2]='pass'
#         #                 temp_dict[3]='fail'
#         #             else:
#         #                 temp_dict[1]='pass'
#         #                 temp_dict[2]='pass'
#         #                 temp_dict[3]='pass'
#         #     context[str(x+1)]=temp_dict
#         #
#         #
#         #
#         # return render(request, 'search.html',{'context':context})
#
#     return render(request, 'search.html')
