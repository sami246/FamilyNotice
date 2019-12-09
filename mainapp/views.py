from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from . import views
from .models import *
from .forms import *
from django.core.serializers import serialize
import json

# Create your views here.
def index(request):
    context = {
        'response' : 'You are in the index page',
    }

    return render(request,'mainapp/index.html' ,{})

def login(request):
	loginForm = LoginForm()

	return render(request,'mainapp/loginPage.html' ,{'form':loginForm,})

def lists_json(request):
    return JsonResponse({
        'list' : list(List.objects.values()),
    })

def tasks(request, List_id):
    if request.method == 'POST':
        print("POST")
		# user = User.objects.get(username = request.user)
		# member = Member.objects.get(user__exact =user.id)
		# print(member)
		# print(List_id)
		# item = Item.objects.get(pk = List_id)
        #
		# price = float(request.POST['price'])
        #
		# print(price)
		# if(price <= item.price):
		# 	return HttpResponse('invalid bid, price too low')
		# item.price = price
		# item.highest_bidder = member
		# item.save()
		# print(item)
		# bid = Bid.objects.create(item = item, bidder = member, price = price)
		# return redirect('home')
        #
		# return HttpResponse('invalid bid')
    else:
        print(List_id)
        instance = get_object_or_404(List, pk=List_id)
        print(instance)
        taskSet = instance.task.all()
        permission_serialize= json.loads(serialize('json', taskSet))
        print("i am still working")
    return render(request,'mainapp/tasks.html' ,{'tasks' : permission_serialize,})

@csrf_exempt
def delete_list(request):
    try:
        value1 = list(request)
        print(value1)
        stvalue = str(value1)
        splitValue = stvalue.split("'")
        List_id = int(splitValue[1])

        instance = List.objects.get(pk=List_id)
        print(instance)
        instance.delete()
        return JsonResponse({
            'response' : 'return response from delete member function',
            'values' : List_id,
        })
    except:
        Http404(request)

def todolist(request):
    context = {
        'response' : 'You are in the index page',
    }

    return render(request,'mainapp/todolists.html' ,{})
