from django.core.exceptions import ValidationError
from django.db.models import query
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




#include models
from .models import Employee, Job, Candidate, Feedback, Field
from .models import TestModel

#include forms
from .forms import CandidateForm, UploadJdForm
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
        return render(request, "users/login.html")
    return HttpResponseRedirect(reverse('index'))


def add_candidate_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")

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

def upload_jd_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")
    username = request.user.username
    user = Employee.objects.get(email=username)
    if request.method == 'POST':
        #if someone forcefully entered raised_by_field using tampering of form
        if 'raised_by_employee' in request.POST:
            raise ValidationError('FORM IS TAMPERED')
        # print(request.POST)
        form = UploadJdForm(request.POST, request.FILES, initial={'raised_by_employee':user})
        form.fields['raised_by_employee'].disabled = True
        if form.is_valid():
            # print(form.cleaned_data)
            obj = form.save()
            return redirect('home_page')
    else:
        form = UploadJdForm(initial={'raised_by_employee':user})
        form.fields['raised_by_employee'].disabled = True
    context = {
        'form' : form
    }
    return render(request, 'upload_jd.html', context)

def home_view(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")
    user_id = 101   # it is currently hardcoded but will be derived from login page itself
    request.session['user_id'] = user_id
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
                'query_set': query_set
            }
            return render(request, 'home.html', context)
        elif 'upload_jd_button' in request.POST:
            return redirect('upload_jd_page')
        elif 'search_candidate_button' in request.POST:
            return redirect('search_candidate')
        else:
            return Http404('Page Not Exist')
    return render(request,'home.html')

def search_jd_view(request, requisition_id):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")
    obj = Job.objects.get(requisition_id=requisition_id)
    if obj is not None:
        context = {
            'obj': obj
        }
        return render(request, 'jd_results.html', context)
    else:
        raise Http404("JD is not exist")


def test_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")
    if request.method == 'POST':
        # print(request.POST)
        form = TestForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj = TestForm()
    else:
        form = TestForm(initial={'field1': 'initial_val'})
        form.fields['field1'].readonly = True
        # print(form.fields['field1'].readonly)
        form.fields['field1'].disabled = True
    context = {
        'form' : form
    }
    return render(request, 'test.html', context)


def login_view(request):
    if request.method == 'POST':

        form = LoginForm(data=request.POST)
        if form.is_valid():

            return render(request,'SignUp_Login/dashboard.html')
    else:
        form = LoginForm()
    return render(request, 'Signup_Login/login.html', {'form': form})


def signup_view(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignUpForm()
    return render(request, 'SignUp_Login/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')



def dashboard(request):
    return render(request, "SignUp_Login/dashboard.html")


def search_candidate(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")

    if request.method == 'POST' or kwargs:
        if request.method == 'GET' and kwargs:
            if not kwargs['candidate_email']:
                raise ValidationError('Get request has arguments type which are not supported')
            candidate_email = kwargs['candidate_email']
        elif request.method == 'POST':
            candidate_email= request.POST['search_element']

        req_id = list(set(Feedback.objects.filter(candidate_email = candidate_email).values_list('requisition_id').order_by('-requisition_id')))
        if len(req_id)==0 :
            return render(request, 'search.html',{'error_message':'There are no results for this input'})

        print(type(req_id))
        print(req_id)

        context = {}
        for x in range(len(req_id)):
            temp_dict={}
            print(type(req_id[x][0]))
            l1=Feedback.objects.get(requisition_id=req_id[x][0],candidate_email=candidate_email, level = 1).status

            temp_dict['req_id']=req_id[x][0];
            temp_dict['email']=candidate_email;
            temp_dict['resume'] = Candidate.objects.get(email=candidate_email).resume
            if l1=='pending':
                temp_dict[1]='pending'
                temp_dict[2]='-'
                temp_dict[3]='-'
            elif l1=='fail':
                temp_dict[1]='fail'
                temp_dict[2]='NA'
                temp_dict[3]='NA'
            else :
                l2=Feedback.objects.get(requisition_id=req_id[x][0],candidate_email=candidate_email, level = 2).status
                if l2=='pending':
                    temp_dict[1]='pass'
                    temp_dict[2]='pending'
                    temp_dict[3]='-'
                elif l1=='fail':
                    temp_dict[1]='pass'
                    temp_dict[2]='fail'
                    temp_dict[3]='NA'
                else :
                    l3=Feedback.objects.get(requisition_id=req_id[x][0],candidate_email=candidate_email, level = 3).status
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
            context[str(x)]=temp_dict



        return render(request, 'search.html',{'context':context})

    return render(request, 'search.html')


def feedback(request, req_id, email_id, level):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")

    if request.method == "POST":
        status = request.POST['status']
        comments = request.POST['comments']
        interviewer_id = Employee.objects.get(email=request.user._wrapped.username).employee_id

        feedback_object = Feedback.objects.get(candidate_email=email_id, requisition_id=req_id, level=level)
        feedback_object.status=status
        feedback_object.interviewer_id = Employee.objects.get(employee_id=interviewer_id)
        feedback_object.comments = comments
        feedback_object.datetime = datetime.now()
        feedback_object.save()

        candidate_email=email_id
        return redirect('../../../../search_candidate/'+str(candidate_email))

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

        basic_detail={
                    'Name' :candidate_name,
                    'Email':email_id,
                    'Graduation_CGPA':candidate_cgpa,
                    'University_name':candidate_college_name,
                    'interviewer_id':interviewer_id,
                    'feedback_id' : feedback_id,
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
            interviewer_id = feedback_object_1.interviewer_id
            feedback_id_1 = feedback_object_1.pk
            last_update_time = feedback_object_1.timestamp

            field_object_1 = Field.objects.all().filter(feedback_id = feedback_id_1)
            field_names = [obj.field_name for obj in field_object_1]
            field_values = [obj.rating for obj in field_object_1]
            level_1 = { 'status': status,
                        'comments' : comments,
                        'interviewer_id': interviewer_id,
                        'details' : zip(field_names, field_values),
                        'timestamp' : last_update_time,
                        'feedback_id_1': feedback_id_1,
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
            comments = feedback_object_1.comments
            interviewer_id = feedback_object_1.interviewer_id
            feedback_id_1 = feedback_object_1.pk
            last_update_time = feedback_object_1.timestamp

            field_object_1 = Field.objects.all().filter(feedback_id = feedback_id_1)
            field_names = [obj.field_name for obj in field_object_1]
            field_values = [obj.rating for obj in field_object_1]

            feedback_object_2 = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id)
            status_ = feedback_object_2.status
            comments_ = feedback_object_2.comments
            interviewer_id_ = feedback_object_2.interviewer_id
            feedback_id_2 = feedback_object_2.pk
            last_update_time_ = feedback_object_2.timestamp

            field_object_2 = Field.objects.all().filter(feedback_id = feedback_id_2)
            field_names_ = [obj.field_name for obj in field_object_2]
            field_values_ = [obj.rating for obj in field_object_2]

            level_1 = { 'status': status,
                        'comments' : comments,
                        'interviewer_id' : interviewer_id,
                        'details' : zip(field_names, field_values),
                        'timestamp' : last_update_time,
                        'feedback_id': feedback_id_1,
                        }

            level_2 = { 'status': status_,
                        'comments' : comments_,
                        'interviewer_id': interviewer_id_,
                        'details' : zip(field_names_, field_values_),
                        'timestamp': last_update_time_,
                        'feedback_id' :feedback_id_2,
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
        return render(request, "users/login.html")

    if request.method == 'POST':
        status=request.POST['status']
        comments=request.POST['comments']

        obj_ = Feedback.objects.get(pk=feedback_id)
        obj_.status = status
        obj_.comments = comments
        obj_.save()

        candidate_email=email_id
        return redirect('../../../../../search_candidate/'+str(candidate_email))


    # try:
    obj= Feedback.objects.get(pk = feedback_id)
    status = obj.status
    comments = obj.comments
    field_object = Field.objects.all().filter(feedback_id = obj)
    field_names= [obj_.field_name for obj_ in field_object]
    field_values= [obj_.rating for obj_ in field_object]
    level_ = obj.level

    Context = {
        'status': status,
        'comments': comments,
        'fields': zip(field_names, field_values),
        'level' : level_,
    }
    return render(request, 'registration/edit.html', Context)
    # except:
    #     return HttpResponse('No details Found')

def field_view(request, req_id, email_id, level, feedback_id):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")

    if request.method == 'POST':
        form = FieldForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('../../')

def delete_field(request, req_id, email_id, level, field_name, del_level):
    feedback_id = Feedback.objects.get(candidate_email=email_id, requisition_id=req_id, level =del_level).pk
    obj = Field.objects.get(feedback_id = feedback_id, field_name = field_name)
    obj.delete()
    if(level == del_level):
        return redirect('../')
    return redirect(f'../edit{feedback_id}')

def test(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")

    return HttpResponse('inside the test')
