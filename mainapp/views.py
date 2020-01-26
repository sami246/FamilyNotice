from django.shortcuts import render, get_object_or_404, redirect
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

# def family_required(f):
#     def familyCheck(request):
#         print(request.session.get('family_session', None))
#         if request.session.get('family_session', None):
#             print("success")
#             f(request)
#             return familyCheck
#         else:
#             return redirect('index')

# Create your views here.
@login_required
def index(request):
    context = {
        'response' : 'You are in the index page',
    }
    return render(request,'mainapp/index.html' ,{})

def login(request):
	loginForm = LoginForm()

	return render(request,'mainapp/loginPage.html' ,{'form':loginForm,})



@login_required
def choose_family(request):
    if request.method == 'POST':
        print('mans trying to post')
        request.session['family_session'] = request.POST['family']
        return redirect('index')
    print(request.user)
    user = User.objects.get(username = request.user)
    print(user)
    mem = Member.objects.get(user = user)
    print(mem)
    # family = Family.objects.get(members = mem)
    familyfilter = Family.objects.filter(members = mem)
    print(familyfilter)
    fam = json.loads(serialize('json', familyfilter))
    return render(request,'mainapp/chooseFamily.html', {'families' : fam})

def lists_json(request):

    family_session = request.session['family_session']
    print("the family currently being used is:")
    print(family_session)
    # family = Family.objects.get(members = mem)
    familyfilter = Family.objects.get(nameofFamily = family_session)
    print(familyfilter)
    print(List.objects.filter(family = familyfilter))
    lists = List.objects.filter(family = familyfilter)
    permission_serialize= json.loads(serialize('json', lists))
    # list(List.objects.values())

    return JsonResponse({
        'list' : permission_serialize,
    })

def complete_status(request):
    value1 = list(request)
    print(value1)
    stvalue = str(value1)
    splitValue = stvalue.split("'")
    Task_id = int(splitValue[1])

    instance = Task.objects.get(pk=Task_id)
    print(instance.completed)
    if(instance.completed==True):
        instance.completed = False
        statusChanged = False
    else:
        instance.completed = True
        statusChanged = True
    instance.save()
    return JsonResponse({
        'name' : instance.name,
        'status' : statusChanged,
        'id' : Task_id,
    })



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        DOB = request.POST['DOB']
        typeU = request.POST['typeOfUser']
        user = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email)
        user.set_password(password)
        user.save()
        member = Member(user = user, dateOfBirth=DOB, userType = typeU)
        member.save()
        user = authenticate(username=username, password=password)
        return redirect('login')
    return render(request,'mainapp/register.html')

@login_required
def tasks(request, List_id):
    if request.method == 'POST':
        print("POST NEW TASK")
        newTask = request.POST['TaskName']
        print(newTask)
        list = List.objects.get(pk=List_id)
        print("List:")
        print(list)
        NewTask = Task(
        name=newTask)
        NewTask.save()
        list.task.add(NewTask)
        list.save()

        return JsonResponse({
            'name' : newTask,
            'id' : NewTask.id,
        })
    else:
        print(List_id)
        instance = get_object_or_404(List, pk=List_id)
        print(instance)
        taskSet = instance.task.all()
        permission_serialize= json.loads(serialize('json', taskSet))
        print("i am still working")
        # completed = permission_serialize.fields.completed
        print(permission_serialize)
    return render(request,'mainapp/tasks.html' ,{'tasks' : permission_serialize, 'ListID': List_id})

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


@csrf_exempt
def delete_task(request):
    try:
        value1 = list(request)
        print(value1)
        stvalue = str(value1)
        splitValue = stvalue.split("'")
        Task_id = int(splitValue[1])

        instance = Task.objects.get(pk=Task_id)
        print(instance)
        instance.delete()
        return JsonResponse({
            'response' : 'return response from delete member function',
            'taskID' : Task_id,
        })
    except:
        Http404(request)


@login_required
def todolist(request):
    context = {
        'response' : 'You are in the index page',
    }

    return render(request,'mainapp/todolists.html' ,{})
