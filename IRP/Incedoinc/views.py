from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('Welcome to Incedo Portal')

def create_candidate_view(request, *args, **kwargs):
    if request.method == 'POST':
        form_fields = request.POST
        print(form_fields)
        
    context = {}
    return render(request, 'create_candidate.html', context)