from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    response = 'You are in the index page'
    return HttpResponse(response)

def login(request):
	loginForm = LoginForm()

	return render(request,'mainapp/loginPage.html' ,{'form':loginForm,})
