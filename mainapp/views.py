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


def create_family(request):
    if request.method == 'POST':
        form = FamilyForm(request.POST)
        if form.is_valid():
            fam = form.save()
            meal = MealWeek(family=fam)
            meal.save()
            fam.mealPlan = meal
            fam.save()
            redirect('choose family')
    Form = FamilyForm()
    return render(request,'mainapp/createFamily.html' ,{'form': Form,})

def current_members(request):
    family_session = request.session['family_session']
    familyfilter = Family.objects.get(nameofFamily = family_session)
    members = Member.objects.filter(family = familyfilter)

    context = {
        'members' : members
    }
    return render(request,'mainapp/currentMembers.html' ,context)

@login_required
def choose_family(request):
    if request.method == 'POST':
        request.session['family_session'] = request.POST['family']
        return redirect('index')
    user = User.objects.get(username = request.user)
    mem = Member.objects.get(user = user)
    # family = Family.objects.get(members = mem)
    familyfilter = Family.objects.filter(members = mem)
    fam = json.loads(serialize('json', familyfilter))
	# view will capture a GET parameter q.
    # url_parameter = request.GET.get("q")
    # print(url_parameter)
    # # If url_parameter’s value isn’t None, it means that some string was passed after ?q= and we want to filter for Artist objects containing this string.
    # if url_parameter:
    #     item = Family.objects.filter(nameofFamily__icontains=url_parameter)
    # else:
    #     item = Family.objects.filter()
    # if request.is_ajax():
    #     html = render_to_string(
    #         template_name="mainapp/fam.html",
    #         context={"item": item}
    #     )
    #     data_dict = {"html_from_view": html}
    #     # It has a single key html_from_view. This key’s value is going to be the variable html.
    #     return JsonResponse(data=data_dict, safe=True)
    return render(request,'mainapp/chooseFamily.html', {'families' : fam})

def lists_json(request):
    user = User.objects.get(username = request.user)
    mem = Member.objects.get(user = user)
    profile_pic = str(mem.profilePic)
    family_session = request.session['family_session']
    # family = Family.objects.get(members = mem)
    familyfilter = Family.objects.get(nameofFamily = family_session)
    lists = List.objects.filter(family = familyfilter)
    permission_serialize= json.loads(serialize('json', lists))
    # list(List.objects.values())
    arr = []
    for list in lists:
        arr.append(list.taskCompleted)

    return JsonResponse({
        'list' : permission_serialize,
        'pic_url' : profile_pic,
        'arr': arr,
    })

def search_key(request):
    user = User.objects.get(username = request.user)
    mem = Member.objects.get(user = user)
    familyfilter = Family.objects.filter(members = mem)
    fam = json.loads(serialize('json', familyfilter))
    FamKey = request.GET['FamKey']
    print(FamKey)
    filter = Family.objects.filter(FamKey = FamKey)
    filteredfams = json.loads(serialize('json', filter))
    return render(request,'mainapp/chooseFamily.html', {'families' : fam, 'response' : filteredfams})

def leave_family(request, Fam):
    user = User.objects.get(username = request.user)
    mem = Member.objects.get(user = user)
    family = Family.objects.get(pk=Fam)
    print(Fam)
    family.members.remove(mem)
    return redirect('choose family')

def join_family(request, Fam_id):
    user = User.objects.get(username = request.user)
    mem = Member.objects.get(user = user)
    family = Family.objects.get(pk=Fam_id)
    print('FAMILY')
    print(family)
    family.members.add(mem)
    family.save()
    return redirect('choose family')

def create_list(request):
    if request.method == 'POST':
        family_session = request.session['family_session']
        fam = Family.objects.get(nameofFamily = family_session)
        form = ListForm(request.POST)
        if form.is_valid():
            list = form.save()
            fam.lists.add(list)
            fam.save()
            return redirect('tasks', list.id)
    list = ListForm()
    context = {'form': list}
    return render(request,'mainapp/createList.html', context)

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
    return render(request,'mainapp/tasks.html' ,{'tasks' : permission_serialize, 'ListID': List_id, 'list':instance})

@csrf_exempt
def delete_list(request, List_id):
    try:
        print(List_id)
        instance = List.objects.get(pk=List_id)
        print(instance)
        instance.delete()
        return redirect('todolists')
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

@login_required
def meal_planner(request):
    family_session = request.session['family_session']
    familyfilter = Family.objects.get(nameofFamily = family_session)
    meals = MealWeek.objects.get(family = familyfilter)
    context = {
        'meals' : meals,
    }
    return render(request,'mainapp/mealPlanner.html', context)

@login_required
def addmeal2(request):
    if request.method == 'POST':
        text = request.POST['text']
        desc = request.POST['description']
        type = request.POST['mealType']
        print('#######################')
        print(type)
        newMeal = MealDesc(description=desc, text=text)
        newMeal.save()
        family_session = request.session['family_session']
        familyfilter = Family.objects.get(nameofFamily = family_session)
        meals = MealWeek.objects.get(family = familyfilter)
        if type == 'monB':
            meals.monB = newMeal
        if type == 'monL':
            meals.monL = newMeal
        if type == 'monD':
            meals.monD = newMeal
        if type == 'tueB':
            meals.tueB = newMeal
        if type == 'tueL':
            meals.tueL = newMeal
        if type == 'tueD':
            meals.tueD = newMeal
        if type == 'wedB':
            meals.wedB=newMeal
        if type == 'wedL':
            meals.wedL=newMeal
        if type == 'wedD':
            meals.wedD=newMeal
        if type == 'thuB':
            meals.thuB=newMeal
        if type == 'thuL':
            meals.thuL=newMeal
        if type == 'thuD':
            meals.thuD=newMeal
        if type == 'friB':
            meals.friB=newMeal
        if type == 'friL':
            meals.friL=newMeal
        if type == 'friD':
            meals.friD=newMeal
        if type == 'satL':
            meals.satL=newMeal
        if type == 'satB':
            meals.satB=newMeal
        if type == 'satD':
            meals.satD=newMeal
        if type == 'sunB':
            meals.sunB=newMeal
        if type == 'sunL':
            meals.sunL=newMeal
        if type == 'sunD':
            meals.sunD=newMeal
        meals.save()
        # newDay = MealWeek(type=newMeal)
        # newDay.save()
        return redirect('meal planner')

@login_required
def deleteMeal(request):
    value1 = list(request)
    stvalue = str(value1)
    splitValue = stvalue.split(":")
    print(splitValue)
    MealTyp = splitValue[1]
    print(MealTyp)
    Meal_id = int(splitValue[2])
    meal = MealDesc.objects.get(pk = Meal_id)
    meal.delete()
    return JsonResponse({
        'meal_id' : Meal_id,
        'meal_type' : MealTyp,
    })

@login_required
def addmeal(request, meal):

    form = MealEntryForm()
    context = { 'form' : form, 'meal':meal,}
    print(meal)
    return render(request,'mainapp/newMeal.html', context)
