from django.shortcuts import render
from django.http import HttpResponse



#include forms
from .forms import Candidate_details_form


# Create your views here.
def index(request):
    return HttpResponse('Welcome to Incedo Portal')

def create_candidate_view(request, *args, **kwargs):
    if request.method == 'POST':
        form_fields = request.POST
        print(form_fields)
    context = {}
    return render(request, 'create_candidate.html', context)

def add_candidate_view(request, *args, **kwargs):
    candidate_details_form = Candidate_details_form()
    context = {
        'candidate_details_form' : candidate_details_form
    }
    return render(request, 'add_candidate.html', context)

