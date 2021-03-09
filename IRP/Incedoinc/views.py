import warnings
warnings.filterwarnings('ignore')
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import query , Q
from django.shortcuts import redirect, render
from decimal import Context
from django.contrib.auth.backends import UserModel
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import LoginForm, SignUpForm, FieldForm, EditCandidateForm, RequisitionCandidateForm
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
import shutil
import pdfkit
from datetime import date as date_
# from resume_parser import resumeparse

#include models
from .models import Employee, Job, Candidate, Feedback, Field, JD, RequisitionCandidate
from .models import TestModel

#include forms
from .forms import CandidateForm, UploadJdForm, UploadJobForm, ResumeForm, EditCandidateForm , CandidateAndReferForm
from .forms import TestForm

from django.conf import settings
from urllib.parse import non_hierarchical, unquote
import logging

logging.basicConfig(filename= 'AuditLog.html', level = logging.INFO, 
    format = '%(asctime)s: %(message)s ')




from django.http import FileResponse

def file_view(request, file_url):
    full_path = os.path.join(settings.BASE_DIR, file_url[1:])
    file_name = file_url.split('/')[-1]
    file_extension = file_name.split('.')[-1].lower()
    # print('-----------------------------file-view----------------------------')
    # print('file_url:', file_url)
    # print('file_name:', file_name)
    # print('full_path:', full_path)
    # print('file_extension:', file_extension)
    # print('------------------------------------------------------------------')
    if file_extension == 'pdf':
        with open(full_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(),content_type='application/pdf')
            response['Content-Disposition'] = 'filename='+file_name
            return response
    else:
        return FileResponse(open(full_path, 'rb'))


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return HttpResponseRedirect(reverse('first_page'))

def delete_jd_view(request, jd_pk):
    query = JD.objects.get(pk=jd_pk)
    jd_name = query.jd_name
    query.jd_file.delete()
    query.delete()
    user = Employee.objects.get(email=request.user.username)
    logging.info( ' deleted JD with query')   
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
    search_query = request.POST.get('search_query') or ''
    context = {}

    if request.method == 'GET' and 'jd_name' in request.GET:
        search_query = request.GET['jd_name']
        query_set = JD.objects.filter(jd_name = search_query)
        context = {
            'query_set' : query_set
        }

    elif request.method == 'GET' and 'deleted' in request.GET:
        msg = 'JD ( '+request.GET['deleted']+' ) is deleted'
        context = {
            'msg' : msg
        }

    if request.method == 'POST':
        if 'home_button' in request.POST:
            return redirect('home_page')

        elif 'search_button' in request.POST:
            search_query = request.POST['search_query']
            if search_query == '':
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

        elif 'list_all_button' in request.POST:
            query_set = JD.objects.all()
            context = {
                'query_set': query_set
            }

        elif 'upload_jd_button' in request.POST:
            return redirect('upload_jd_page')

        elif 'delete_jd_button' in request.POST:
            return HttpResponse('<h1>delete jd</h1>')

    context['search_query'] = search_query
    return render(request, 'manage_jd.html/', context)

    return HttpResponse('<h1>this is managejd</h1>')


def manage_job_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return render(request, 'login')
    request.session['prev_url'] = 'manage-job/'

    query_set = None
    msg = None
    search_query = request.POST.get('search_query') or ''
    checkboxes = {
        'open_to_list' : [],
        'status_list' : [],
    }

    context = {
        'query_set' : None,
        'sub_query_set' : None,
        'msg' : None,
        'checkboxes' : checkboxes,
        'search_query' : search_query,
    }

    if request.method == 'GET' and 'requisition_id' in request.GET:
        search_query = request.GET['requisition_id']
        query_set = Job.objects.filter(requisition_id = search_query)
        context['query_set'] = query_set

    # elif request.method == 'GET' and 'expand_token' in request.GET:
    #     expand_token = request.GET['expand_token']
    #     query_set = Job.objects.all()
    #     sub_query_set = RequisitionCandidate.objects.filter(requisition_id=expand_token)
    #     context['query_set'] = query_set
    #     context['expand_token'] = expand_token
    #     context['sub_query_set'] = sub_query_set

    elif request.method == 'GET' and 'deleted' in request.GET:
        msg = 'Requisition ( ' + request.GET['deleted'] + ' ) is Deleted'
        context['msg'] = msg

    elif request.method == 'POST':
        # print('------------------------manage-job | post -------------------')
        # print(request.POST)
        # request.session['open_to_internal'] = request.POST.get('open_to_internal', [])
        # request.session['requisition_status'] = request.POST.get('requisition_status', [])

        if 'home_button' in request.POST:
            return redirect('home_page')

        if 'search_button' in request.POST:
            search_query = request.POST.get('search_query', '')
            open_to_list = request.POST.getlist('open_to_list')
            status_list = request.POST.getlist('status_list')
            checkboxes['open_to_list'] = open_to_list
            checkboxes['status_list'] = status_list

            if search_query == '':
                msg = 'Enter something to search'
                context['msg'] = msg

            else:
                query_set = Job.objects.all()
                if len(open_to_list)!=0:
                    query_set = query_set.filter(open_to_internal__in=open_to_list)
                if len(status_list) != 0:
                    query_set = query_set.filter(requisition_status__in=status_list)
                query_set = query_set.filter(Q(requisition_id__icontains=search_query)
                                            | Q(jd__jd_name__icontains=search_query)
                                            | Q(requisitioncandidate__candidate_email__f_name__icontains=search_query)
                                            | Q(position_owner_id__full_name__icontains=search_query)
                                            | Q(raised_by_employee__full_name__icontains=search_query)
                            ).distinct()
                context['query_set'] = query_set


        elif 'list_all_button' in request.POST:
            open_to_list = request.POST.getlist('open_to_list')
            status_list = request.POST.getlist('status_list')
            checkboxes['open_to_list'] = open_to_list
            checkboxes['status_list'] = status_list
            query_set = Job.objects.all()
            if len(open_to_list)!=0:
                query_set = query_set.filter(open_to_internal__in=open_to_list)
            if len(status_list) != 0:
                query_set = query_set.filter(requisition_status__in=status_list)
            context['query_set'] = query_set

        elif 'raise_requisition_button' in request.POST:
            return redirect('upload_job_page')

    req_cand_dict = {}
    if query_set:
        for job_obj in query_set:
            req = job_obj.requisition_id
            req_cand_dict[req] = RequisitionCandidate.objects.filter(requisition_id = job_obj)
    context['req_cand_dict'] = req_cand_dict

    return render(request, 'manage_job.html/', context)

def upload_jd_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")
    username = request.user.username
    user = Employee.objects.get(email=username)
    if request.method == 'POST':
        #if someone forcefully entered raised_by_field using tampering of form
        if 'uploaded_by_employee' in request.POST:
            raise ValidationError('FORM IS TAMPERED')
        form = UploadJdForm(request.POST, request.FILES, initial={'uploaded_by_employee':user})
        form.fields['uploaded_by_employee'].disabled = True
        if form.is_valid():
            obj = form.save(commit=False)
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
        current_user = request.user
        logging.info('Yaha to pahuch gaye beta ji')
        username = request.user.username
        user = Employee.objects.get(email=username)
        logging.info( user,' logged in')  
        logging.warning('Hello, I am logging from the Home Page! User =',current_user)
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

from django.core.files.storage import FileSystemStorage, DefaultStorage
from django.core.files import File

def add_candidate_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')
    

    form_ = ResumeForm()
    form=None
    referral_requisition_id_obj=None
    if 'referral_requisition_id' in request.session:
        referral_requisition_id_obj=Job.objects.get(requisition_id=request.session['referral_requisition_id'])
        form = CandidateForm(initial={'registered_by': user , 'requisition_id' : referral_requisition_id_obj})
        form.fields['registered_by'].disabled = True
        form.fields['requisition_id'].disabled = True
    else:
        form = CandidateForm(initial={'registered_by': user})
        form.fields['registered_by'].disabled = True
    context = {}
    if request.method == 'POST' and 'form_' in request.POST:
        # print('-----------------method=post|resume_form---------------------')
        # print(request.POST)
        # print(request.FILES)
        # print('-------------------------------------------------------------')
        form_ = ResumeForm(request.POST, request.FILES)
        if form_.is_valid():
            # print('----------form_ is valid-----------------')
            resume = request.FILES['resume']
            fs = FileSystemStorage()
            resume_name = fs.save(f'temp_resume/{resume.name}', resume)
            # uploaded_file_url = fs.url(resume_name)
            uploaded_file_url = '/media/'+resume_name
            # print('test url ', f'{fs.url(resume_name)}')

            request.session['resume_file_name'] = resume_name
            request.session['resume_file_url'] = uploaded_file_url
            # print('---------------saved file details-----------------')
            # print('resume_name', resume_name)
            # print('uploaded_file_url', uploaded_file_url)
            # print('-----------------------------------------------')
            try:
                data = resumeparse.read_file(f'media/{resume_name}')
                full_name = data['name'].split(' ')
                f_name = ''
                m_name = ''
                l_name = ''
                if len(full_name) == 1:
                    f_name = full_name[0]
                elif len(full_name) == 2:
                    f_name = full_name[0]
                    l_name = full_name[1]
                else:
                    f_name = full_name[0]
                    l_name = full_name[len(full_name)-1]
                    m_name = full_name[1]
                initial_value_dict={'registered_by': user,
                                            'f_name' : f_name,
                                            'm_name' : m_name,
                                            'l_name' : l_name,
                                            'email' : data['email'],
                                            'mobile' : data['phone'][-10:],
                                            # 'resume' : file_obj,
                                            'experience' : data['total_exp'],
                                            # 'college_name' : data['university'][0],
                                            }
                if referral_requisition_id_obj is not None:
                    initial_value_dict['requisition_id']=referral_requisition_id_obj

                form = CandidateForm(initial=initial_value_dict)
                form.fields['registered_by'].disabled = True

                if referral_requisition_id_obj is not None:
                    form.fields['requisition_id'].disabled = True
            except:
                pass

            form_ = None
        # return render(request, 'forms/add_candidate.html', {'form':form, 'form_':form_, 'resume_name': uploaded_file_url})

    elif request.method == 'POST' and 'email' in request.POST:
        # resume_name = request.POST['resume_name']
        # resume_name = resume_name.lstrip('/')
        # resume_name = resume_name.replace('%20', ' ')
        # print(resume_name, '========================================')
        # with open(f'media/{resume_name}') as resume_file:

        resume_name = request.session['resume_file_name']
        uploaded_file_url = request.session['resume_file_url']
        if referral_requisition_id_obj is not None:
            form = CandidateForm(request.POST, initial={'registered_by': user , 'requisition_id':referral_requisition_id_obj})
            form.fields['registered_by'].disabled = True
            form.fields['requisition_id'].disabled = True
        else:
            form = CandidateForm(request.POST, initial={'registered_by': user})
            form.fields['registered_by'].disabled = True
        if form.is_valid():
            # print('---------------Candidate Form is Valid------------------')
            # print('resume_name', resume_name)
            # print('uploaded_file_url', uploaded_file_url)
            # print('--------------------------------------------------------')
            del request.session['resume_file_name']
            del request.session['resume_file_url']

            candidate_obj = form.save(commit=False)

            with open(uploaded_file_url.lstrip('/'), "rb") as f:
                candidate_obj.resume.save(uploaded_file_url.split('/')[-1], File(f))
                # print('--------------inside open-----------------')
                # print('f', f)
                # print('candidate_obj.file.name', candidate_obj.resume.name)
                # print('candidate_obj.file.url', candidate_obj.resume.url)
                # print('------------------------------------------')


            # if os.path.exists('media/temp_resume'):
            #     shutil.rmtree('media/temp_resume')

            candidate_email = form.cleaned_data['email']
            if referral_requisition_id_obj is not None:
                job_obj=referral_requisition_id_obj
            else:
                requisition_id = form.cleaned_data['requisition_id']
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
            requisition_candidate_obj=RequisitionCandidate.objects.create(
                requisition_id = job_obj,
                candidate_email = candidate_obj,
                candidate_status = 'In-Progress',
            )
            if referral_requisition_id_obj is not None:
                print(requisition_candidate_obj)
                requisition_candidate_obj.referred_by=user
                requisition_candidate_obj.referred_date=date_.today()
                requisition_candidate_obj.save()
                #######################################################
                #### Code for sending referral mail####################
                #######################################################
                del request.session['referral_requisition_id']
                return redirect('../'+'referrals/refer_candidate/'+str(requisition_candidate_obj.requisition_id)+'/?confirmed='+str(candidate_obj.email))

            return redirect('../'+'search_candidate/?candidate_email='+str(candidate_email))

        form_ = None
        # return render(request, 'forms/add_candidate.html', {'form':form, 'resume_name': request.POST['resume_name']})

    else:
        for field in form.fields:
            form.fields[field].disabled = True

    form.fields['registered_by'].disabled = True
    if 'referral_requisition_id' in request.session:
        form.fields['requisition_id'].disabled = True
    context = {
        'form': form,
        'form_':form_,
        'referral_requisition_id_obj':referral_requisition_id_obj
    }
    return render(request, 'forms/add_candidate.html', context)


def delete_temp(request):
    try:
        if( 'resume_file_url' in request.session):
            cur_url = request.session['resume_file_url'].lstrip('/')
            os.remove(cur_url)
    except:
        pass
    if 'referral_requisition_id' in request.session:
        referral_requisition_id=request.session['referral_requisition_id']
        del request.session['referral_requisition_id']
        return redirect('../referrals/refer_candidate/%s' %str(referral_requisition_id))
    return redirect('search_candidate')


def delete_resume(request, resume_name):
    resume_name = resume_name.replace('%20', ' ')
    try:
        os.remove(f'media/Resume/{resume_name}')
    except:
        return redirect('search_candidate')

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

def print_obj(req_cand_obj):
        print_obj(req_cand_obj)
        print('--------------------obj prev-----------------------')
        print('requisition_candidate_id', req_cand_obj.requisition_candidate_id)
        print('requisition_id', req_cand_obj.requisition_id)
        print('candidate_email' ,  req_cand_obj.candidate_email)
        print('referred_by', req_cand_obj.referred_by)
        print('referred_date', req_cand_obj.referred_date)
        print('expected_doj', req_cand_obj.expected_doj)
        print('actual_doj', req_cand_obj.actual_doj)
        print('status_choices', req_cand_obj.status_choices)
        print('candidate_status', req_cand_obj.candidate_status)
        print('----------------------------obj saved-------------------------')

def view_candidate(request, candidate_email):
    if not request.user.is_authenticated:
        return redirect('login')

    # if request.method == 'GET':
    #     print('-----------------view_candidate | GET REQUEST----------------------')
    #     print(request.GET)
    #     print('-----------------------------------------------------------------')

    # if request.method == 'POST':
    #     print('-----------------view_candidate | POST REQUEST---------------------')
    #     print(request.POST)
    #     print('---------------------------------------------------------------')

    editable_req_id = None
    form_req_cand = None
    try:
        candidate_obj = Candidate.objects.get(email=candidate_email)
    except ObjectDoesNotExist:
        return render(request, 'view_candidate.html', {'error_msg':"Oops :( Candidate Doesn't Exist"})
    except:
        return render(request,'view_candidate.html', {'error_msg':"Oops ;( Something went wrong"})

    if request.method == 'GET' and 'prev_url' in request.GET:
        prev_url = request.GET['prev_url']
    if request.method == 'POST':
        if 'home_button' in request.POST:
            return redirect('home_page')

        elif 'edit_details' in request.POST:
            candidate_obj=Candidate.objects.filter(email=candidate_email)
            return redirect('../../edit_candidate/'+str(candidate_email))

        elif 'editable_req_id' in request.POST:
            editable_req_id = request.POST['editable_req_id']
            req_cand_obj = RequisitionCandidate.objects.get(candidate_email=candidate_obj, requisition_id__requisition_id=editable_req_id)
            form_req_cand = RequisitionCandidateForm(instance=req_cand_obj)
            form_req_cand.fields['requisition_id'].disabled = True
            form_req_cand.fields['referred_by'].disabled = True

        elif 'save_status' in request.POST:
            saved_req_id = request.POST['save_status']
            req_cand_obj = RequisitionCandidate.objects.get(candidate_email=candidate_obj, requisition_id__requisition_id=saved_req_id)
            form_req_cand = RequisitionCandidateForm(request.POST, instance=req_cand_obj)
            form_req_cand.fields['requisition_id'].disabled = True
            form_req_cand.fields['referred_by'].disabled = True
            # form_req_cand['requisition_id'].initial = Job.objects.get(requisition_id=saved_req_id)
            if form_req_cand.is_valid():
                req_cand_obj = form_req_cand.save(commit=False)
                # print(req_cand_obj)
                req_cand_obj.requisition_id = Job.objects.get(requisition_id=saved_req_id)
                req_cand_obj.save()
                # print(req_cand_obj)

            else:
                editable_req_id = saved_req_id

    query_set = RequisitionCandidate.objects.filter(candidate_email=candidate_obj)

    context = {
        'candidate_obj' : candidate_obj,
        'query_set' : query_set,
        'form_req_cand' : form_req_cand,
        'editable_req_id' : editable_req_id,
    }
    return render(request, 'view_candidate.html', context)

def search_candidate(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')
    # request.session['prev_url'] = 'search_candidate/'
    search_query = request.POST.get('search_element') or ''

    if (request.GET and request.GET is not {}) or request.method == 'POST':
        context={}
        if request.method == 'POST':
            if 'home_button' in request.POST:
                return redirect('home_page')
            if 'add_candiate' in request.POST:
                if 'referral_requisition_id' in request.session:
                    del request.session['referral_requisition_id']
                return redirect('../add-candidate/')
            if 'listall' in request.POST:
                temp_list_tuple = list(set((RequisitionCandidate.objects.all())))
                if len(temp_list_tuple)==0:
                    return render(request, 'search.html', {'error_message':'Oops :(   No Candidate Yet', 'search_query':search_query })
                # print(temp_list_tuple,"--------------")
            elif 'search' in request.POST:
                temp_list_tuple = list(set((RequisitionCandidate.objects.filter(
                                                                            Q(requisition_id__in=Job.objects.filter(requisition_id__contains=request.POST['search_element']))
                                                                          | Q(candidate_email__in=Candidate.objects.filter(f_name__contains=request.POST['search_element']))
                                                                        | Q(candidate_email__in=Candidate.objects.filter(m_name__contains=request.POST['search_element']))
                                                                      | Q(candidate_email__in=Candidate.objects.filter(l_name__contains=request.POST['search_element'])) ))))
        elif request.GET and request.GET is not {} :
            candidate_email = ''
            if 'candidate_email' in request.GET:
                candidate_email = request.GET['candidate_email']
            else:
                return render(request, 'search.html',{'error_message':'No Results', 'search_query':search_query })
            if len(candidate_email)==0:
                return render(request, 'search.html',{'error_message':'Please enter something', 'search_query':search_query })
            temp_list_tuple = list(RequisitionCandidate.objects.filter(candidate_email__in=Candidate.objects.filter(email__contains=candidate_email)))
            if len(temp_list_tuple)==0 :
                return render(request, 'search.html',{'error_message':'No matching Candidate for \''+str(candidate_email)+'\'', 'search_query' : search_query })
        # print(len(temp_list_tuple))
        if len(temp_list_tuple)==0 :
            return render(request, 'search.html',{'error_message':'No Results', 'search_query':search_query })
        y=0
        for x in temp_list_tuple:
            # print(x)
            y=y+1
            temp_dict={}
            l1_obj=Feedback.objects.get(requisition_id=x.requisition_id,candidate_email=x.candidate_email, level = 1)
            l2_obj=Feedback.objects.get(requisition_id=x.requisition_id,candidate_email=x.candidate_email, level = 2)
            l3_obj=Feedback.objects.get(requisition_id=x.requisition_id,candidate_email=x.candidate_email, level = 3)

            l1=l1_obj.status
            l3=l2_obj.status
            l2=l3_obj.status
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

            temp_dict['requisition_candidate_obj']=x
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
            context[str(y)]=temp_dict
        # print(context)
        return render(request, 'search.html',{'context':context , 'level_':level_, 'level__':level__, 'l1_id':l1_id, 'l2_id':l2_id, 'l3_id':l3_id , 'search_query':search_query })
    else:
        return render(request, 'search.html', {'search_query': search_query})

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
        status=request.POST['status']
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
    initial_elements={
    'initial_search_element':None,
    'initial_open_internal_yes':None,
    'initial_open_internal_no':None,
    'initial_req_status_open':None,
    'initial_req_status_onhold':None,
    }

    if request.method == 'POST':
        if 'home_button' in request.POST:
             return redirect('home_page')
        elif 'refer_candidate' in request.POST:
            return redirect('../referrals/refer_candidate/%s' %request.POST['refer_candidate'])
        elif 'my_referrals' in request.POST:
            return redirect('../referrals/my_referrals/%s' %Employee.objects.get(email=request.user.username).employee_id)
        elif 'listallopen' in request.POST or 'search' in request.POST:
            open_to_internal_list=['Yes','No']
            if 'open_to_internal' in request.POST:
                open_to_internal_list=request.POST.getlist('open_to_internal')
                if 'Yes' in open_to_internal_list:
                    initial_elements['initial_open_internal_yes']='Yes'
                if 'No' in open_to_internal_list:
                    initial_elements['initial_open_internal_no']='No'
            requisition_status_list=['Open','On-Hold']
            if 'requisition_status' in request.POST:
                requisition_status_list=request.POST.getlist('requisition_status')
                if 'Open' in requisition_status_list:
                    initial_elements['initial_req_status_open']=True
                if 'On-Hold' in requisition_status_list:
                    initial_elements['initial_req_status_onhold']=True
            temp_list_tuple=()
            if 'listallopen' in request.POST:
                temp_list_tuple = list(set(Job.objects.filter(open_to_internal__in=open_to_internal_list ,requisition_status__in=requisition_status_list)))
            elif 'search' in request.POST:
                search_element=request.POST['search_element']
                if(len(search_element)==0):
                    return render(request, 'referrals.html',{'error_message':'Please Enter Something','initial_elements':initial_elements})
                initial_elements['initial_search_element']=search_element
                temp_list_tuple = list(set(Job.objects.filter(Q(requisition_id__contains=search_element , open_to_internal__in=open_to_internal_list ,requisition_status__in=requisition_status_list) | Q(jd__in=JD.objects.filter(jd_name__contains=search_element) , open_to_internal__in=open_to_internal_list ,requisition_status__in=requisition_status_list) | Q(position_owner_id__in=Employee.objects.filter(full_name__contains=search_element) , open_to_internal__in=open_to_internal_list ,requisition_status__in=requisition_status_list))))
            if len(temp_list_tuple)==0:
                return render(request, 'referrals.html',{'error_message':'Oops :( So Empty','initial_elements':initial_elements})
            context={}
            for x in range(len(temp_list_tuple)):
                context[x+1]=temp_list_tuple[x]
            return render(request, 'referrals.html',{'context':context,'initial_elements':initial_elements})

    return render(request, 'referrals.html',{'initial_elements':initial_elements})

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
    return render(request, 'my_referrals.html',{'context':context , 'employee_id':employee_id})


def refer_candidate_view(request,requisition_id):
    if not request.user.is_authenticated:
        return redirect('login')
    if 'home_button' in request.POST:
        return redirect('home_page')
    if 'go_back' in request.POST:
            return redirect('referrals_page')
    job_obj=Job.objects.filter(requisition_id=requisition_id)
    if(len(job_obj)==0):
        return render(request, 'refer_candidate.html',{'error_message':'Oops , Something went wrong!'})
    context={}
    requisition_candidate_obj_dict={}
    initial_search_element=None
    if request.method=='POST':
        # print(request.POST)
        if 'ok' in request.POST:
            return redirect('../../../referrals/refer_candidate/%s' %str(requisition_id))

        if 'yes' in request.POST:
            candidate_obj=Candidate.objects.filter(email=request.POST['yes'])[0]
            RequisitionCandidate.objects.create(
                requisition_id=job_obj[0],
                candidate_email=candidate_obj,
                referred_by=Employee.objects.get(email=request.user.username),
                candidate_status='In-Progress',
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

            # mail_subject = 'New Candidate Referred'
            # message = render_to_string('new_candidate_referred.html', {
            #     'req_id': job_obj[0],
            #     'candidate_email': candidate_obj,
            #     'referred_by':Employee.objects.get(email=request.user.username),
            #
            #
            # })
            # to_email = "kartikey.raut@incedoinc.com"
            # email = EmailMessage(
            #     mail_subject, message, to=[to_email]
            # )
            # email.send()
            return render(request, 'refer_candidate.html',{'job_obj':job_obj[0],'confirmed_message_obj':candidate_obj})
        if 'add_new_refer' in request.POST:
            request.session['referral_requisition_id']=requisition_id
            return redirect('../../../add-candidate')
        if 'refer_this_candidate' in request.POST:
            confirmation_candidate_obj=(Candidate.objects.filter(email=request.POST['refer_this_candidate']))
            if len(confirmation_candidate_obj)==0:
                return render(request, 'refer_candidate.html',{'job_obj':job_obj[0]})
            else:
                return render(request, 'refer_candidate.html',{'job_obj':job_obj[0],'confirmation_candidate_obj':confirmation_candidate_obj[0]})
        if 'search' in request.POST:
            if len(request.POST['search_element'])==0:
                candidate_obj=Candidate.objects.all()
            else:
                initial_search_element=request.POST['search_element']
                candidate_obj=Candidate.objects.filter(Q(f_name__contains=request.POST['search_element'])
                                                     | Q(m_name__contains=request.POST['search_element'])
                                                     | Q(l_name__contains=request.POST['search_element'])
                                                     | Q(email__contains=request.POST['search_element']))
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
    elif request.method=='GET':
        if 'confirmed' in request.GET:
            candidate_obj=Candidate.objects.filter(email=request.GET['confirmed'])[0]
            return render(request, 'refer_candidate.html',{'job_obj':job_obj[0],'confirmed_message_obj':candidate_obj})
    return render(request, 'refer_candidate.html',{'job_obj':job_obj[0],'context':context,'requisition_candidate_obj_dict':requisition_candidate_obj_dict , 'initial_search_element':initial_search_element})


def audit_log_view(request):
    hello = 'my_name'
    if request.method == 'GET':
        return render(request, 'IRP/Incedoinc/templates/AuditLog.html',) 