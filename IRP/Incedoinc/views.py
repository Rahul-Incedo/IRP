from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import HttpResponse



#include forms
from .forms import Candidate_details_form


# Create your views here.
def index(request):
    return HttpResponse('Welcome to Incedo Portal')
    
def add_candidate_view(request, *args, **kwargs):
    candidate_details_form = Candidate_details_form(request.POST or None)
    context = {
        'candidate_details_form' : candidate_details_form
    }
    if request.method == 'POST':
        pass
    return render(request, 'add_candidate.html', context)
