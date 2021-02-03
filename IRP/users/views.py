from django import forms
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import SignUpForm

from django.contrib.auth.models import User

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import LoginForm, SignUpForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User


from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, message
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import re
from django.contrib import messages

UserModel = get_user_model()
from .forms import SignUpForm


# def index(request):
#     return HttpResponse('Vaishnavi here!')




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
        form = LoginForm(data=request.POST)
        return render(request, 'Signup_Login/login.html', {'form': form})
    else:
        return HttpResponse('Activation link is invalid!')


# def login_view(request):
#     if request.method == 'POST':

#         form = LoginForm(data=request.POST)
#         if form.is_valid():

#             return render(request,'SignUp_Login/dashboard.html')  #homepage
#     else:
#         form = LoginForm()
#     return render(request, 'Signup_Login/login.html', {'form': form})




def login_view(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			email = request.POST.get('email')
			password =request.POST.get('password')

			user = authenticate(request, email=email, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'SignUp_Login/login.html', context)




def logout_view(request):
    form = SignUpForm(request.POST)
    return render(request, 'Signup_Login/signup.html', {'form': form}, {'message':'Successfully loged out'})


   





















































# # Create your views here.
# # def index(request):
# #     if not request.user.is_authenticated:
# #         return render(request, "users/login.html")
# #     context = {
# #         "user":request.user
# #     }
# #     return HttpResponseRedirect(reverse('home_page'))
# #     return render(request, "home.html", context)


# def index(request):
#     return HTTPResponse('Vaishnavi\'s Page')

# def login_view(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     #print(username)

#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return HttpResponseRedirect(reverse('index'))
#     else:
#         return render(request, "users/login.html", {"message":"Invalid credential"})

# def signup_view(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user_ = User.objects.create_user(username=str(form.cleaned_data['email']), password=form.cleaned_data['password'])
#             print(user_.username)
#             user_.save()
#             user = form.save()

#             return HttpResponseRedirect(reverse('home_page'))
#     else:
#         form = SignUpForm()
#     return render(request, 'SignUp_Login/signup.html', {'form': form})

# def logout_view(request):
#     logout(request)
#     return render(request, "users/login.html", {'message':'Successfully loged out'})
