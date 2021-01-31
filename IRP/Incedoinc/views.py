from decimal import Context
from django.contrib.auth.backends import UserModel
from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Employee, Job, Candidate, Feedback
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import LoginForm, SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User


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
import re

UserModel = get_user_model()
from .forms import SignUpForm




# Create your views here.
def index(request):
    return render(request, 'rudra_base.html' )


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

    return render(request, 'registration/feedback.html', Context)


def test(request):
    return HttpResponse('inside the test')

# def signup_view(request):
#    if request.method == 'POST':
#        form = SignUpForm(request.POST)
#       if form.is_valid():
#            form.save()
#            return redirect('posts:list')
 #   else:
 #       form = SignUpForm()
  #  return render(request, 'Signup_login/signup.html', {'form': form})


#def login_view(request):
    if request.method == 'POST':
        
        form = LoginForm(data=request.POST)
        if form.is_valid():
            
            return render(request,'SignUp_Login/dashboard.html')
    else:
        form = LoginForm()
    return render(request, 'Signup_Login/login.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        
        form = LoginForm(data=request.POST)
        if form.is_valid():
            
            return render(request,'SignUp_Login/dashboard.html')
    else:
        form = LoginForm()
    return render(request, 'Signup_Login/login.html', {'form': form})




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

    






#user = form.save()
           # username = form.cleaned_data.get('username')
           # raw_password = form.cleaned_data.get('password1')
           # user = authenticate(username=username, password=raw_password)
           # login(request, user)
            
           # return redirect('home')
            #else:
    #    form = SignUpForm()
   # return render(request, 'SignUp_Login/signup.html', {'form': form})
    