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
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings


# def family_required(function):
#     def familyCheck(self):
#         print('In decorator')
#         print(request.session.get('family_session', None))
#         if not request.session['family_session']:
#             return redirect('index')
#         else:
#             print("success")
#             function(self)
#             return familyCheck

@login_required
def index(request):
    context = {
        'response' : 'You are in the index page',
    }
    return render(request,'mainapp/index.html' ,{})

@login_required
def create_family(request):
    if request.method == 'POST':
        form = FamilyForm(request.POST)
        if form.is_valid():
            members = form.cleaned_data['members']
            print(members)
            fam = form.save()
            meal = MealWeek(family=fam)
            meal.save()
            fam.mealPlan = meal
            chatroom = Chatroom(family=fam)
            chatroom.save()
            fam.chatroom = chatroom
            chore_List = ChoreList(family=fam)
            chore_List.save()
            fam.choreList = chore_List
            fam.save()
            fam.members.set(members)
            fam.save()
            return redirect('choose family')
    Form = FamilyForm()
    return render(request,'mainapp/createFamily.html' ,{'form': Form,})

@login_required
def current_members(request):
    try:
        family_session = request.session['family_session']
    except:
        return redirect('choose family')
    familyfilter = Family.objects.get(nameofFamily = family_session)
    members = Member.objects.filter(family = familyfilter)
    mem = Member.objects.get(user = request.user)
    FamiliesJoined = Family.objects.filter(members=mem)
    fam = json.loads(serialize('json', FamiliesJoined))
    context = {
        'members' : members,
        'fam': family_session,
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

    try:
        print(request.session['result'])
    except:
        request.session['result'] = 'false'
    return render(request,'mainapp/chooseFamily.html', {'families' : fam})

@login_required
def lists_json(request):
    user = User.objects.get(username = request.user)
    mem = Member.objects.get(user = user)
    try:
        family_session = request.session['family_session']
    except:
        return redirect('choose family')
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
        'arr': arr,
    })

@login_required
def chat(request):
    try:
        family_session = request.session['family_session']
    except:
        return redirect('choose family')
    familyfilter = Family.objects.get(nameofFamily = family_session)
    members = Member.objects.filter(family = familyfilter)
    chatroom = Chatroom.objects.get(family = familyfilter)
    messages = Message.objects.filter(chatroom = chatroom)
    ordered = messages.order_by('timePublished')
    permission_serialize= json.loads(serialize('json', ordered))
    user = User.objects.get(username = request.user)
    mem = Member.objects.get(user = user)

    mylist = zip(permission_serialize, messages)

    context ={
    'messages': mylist,
    'name' : chatroom,
    'memId' : mem.id,
    'members' : members,
    }
    return render(request,'mainapp/chat.html', context)

@login_required
def add_message(request):
    query = QueryDict(request.body)
    author = query.get('Author')
    message = query.get('OutgoingMessage')
    member = Member.objects.get(id = author)
    authorName = member.user.first_name
    OutgoingMessage = Message(author = member, message= message)
    OutgoingMessage.save()
    try:
        family_session = request.session['family_session']
    except:
        return redirect('choose family')
    familyfilter = Family.objects.get(nameofFamily = family_session)
    chatroom = Chatroom.objects.get(family = familyfilter)
    chatroom.messages.add(OutgoingMessage)

    return JsonResponse({
        'message' : message,
        'authorName' : authorName,
        'time' : OutgoingMessage.timePublished,
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

@login_required
def location(request):
    if request.method == "PUT":
        geolocation = QueryDict(request.body)
        lat = geolocation.get('lat')
        long = geolocation.get('long')
        user = User.objects.get(username = request.user)
        CurrentMem = Member.objects.get(user = user)
        CurrentMem.lat = lat
        CurrentMem.long = long
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y at %H:%M:%S")
        CurrentMem.timeOfLocation = dt_string
        CurrentMem.save()
        print('Geolocation updated')
    user = User.objects.get(username = request.user)
    mem = Member.objects.get(user = user)
    try:
        family_session = request.session['family_session']
    except:
        return redirect('choose family')
    fam = Family.objects.get(nameofFamily = family_session)
    familyMembers = Member.objects.filter(family = fam)
    famMem = json.loads(serialize('json', familyMembers))
    context = {
        'lat' : mem.lat,
        'long' : mem.long,
        'time' : mem.timeOfLocation,
        'inital' : mem.user.first_name[0],
        'fam' : fam
    }
    return render(request,'mainapp/locations.html', context)

@login_required
def location_of_member(request):
    try:
        family_session = request.session['family_session']
    except:
        return redirect('choose family')
    id = request.GET['loc_name']
    print(id)
    mem = Member.objects.get(id = id)
    return JsonResponse({
        'lat' : mem.lat,
        'long' : mem.long,
        'time' : mem.timeOfLocation,
        'inital' : mem.user.first_name[0]
    })

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
    family.members.add(mem)
    family.save()
    return redirect('choose family')

@login_required
def create_list(request):
    if request.method == 'POST':
        try:
            family_session = request.session['family_session']
        except:
            return redirect('choose family')
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

def addchore(request):
    print('IN ADD CHORE')
    # return redirect('chores')
    try:
        family_session = request.session['family_session']
    except:
        return redirect('choose family')
    if request.method == 'POST':
        form = ChoreForm(request.POST)
        if form.is_valid():
            chore = form.save()
            familyfilter = Family.objects.get(nameofFamily = family_session)
            chorelist = ChoreList.objects.get(family=familyfilter)
            chorelist.chores.add(chore)
            chorelist.save()
            return redirect('chores')
    form = ChoreForm()
    context = {
        'form' : form,
    }
    return render(request,'mainapp/addChore.html', context)

def addreward(request):
    print('IN ADD Reward')
    try:
        family_session = request.session['family_session']
    except:
        return redirect('choose family')
    if request.method == 'POST':
        form = RewardForm(request.POST)
        if form.is_valid():
            reward = form.save()
            familyfilter = Family.objects.get(nameofFamily = family_session)
            chorelist = ChoreList.objects.get(family=familyfilter)
            chorelist.rewards.add(reward)
            chorelist.save()
            return redirect('chores')
    form = RewardForm()
    context = {
        'form' : form,
    }
    return render(request,'mainapp/addReward.html', context)

def complete_status(request):
    try:
        family_session = request.session['family_session']
    except:
        return redirect('choose family')
    value1 = list(request)
    stvalue = str(value1)
    splitValue = stvalue.split("'")
    Task_id = int(splitValue[1])
    instance = Task.objects.get(pk=Task_id)
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

from django.contrib.auth.views import LoginView

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        DOB = request.POST['DOB']
        typeU = request.POST['typeOfUser']
        gender = request.POST['genderOfUser']
        user = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email)
        user.set_password(password)
        user.save()
        member = Member(user = user, dateOfBirth=DOB, userType = typeU, genderType=gender)
        member.save()
        user = authenticate(username=username, password=password)
        return redirect('index')
    return render(request,'mainapp/register.html')

@login_required
def tasks(request, List_id):
    try:
        family_session = request.session['family_session']
    except:
        return redirect('choose family')
    if request.method == 'POST':
        newTask = request.POST['TaskName']
        list = List.objects.get(pk=List_id)
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
        instance = get_object_or_404(List, pk=List_id)
        taskSet = instance.task.all()
        permission_serialize= json.loads(serialize('json', taskSet))
    return render(request,'mainapp/tasks.html' ,{'tasks' : permission_serialize, 'ListID': List_id, 'list':instance})

@csrf_exempt
def delete_list(request, List_id):
    try:
        instance = List.objects.get(pk=List_id)
        instance.delete()
        return redirect('todolists')
    except:
        Http404(request)

@login_required
def share_key(request):
    emails = request.POST['emails']
    email_arr = emails.split(",")
    family = request.POST.getlist('fam_Key', False)
    ListOfFamilies = ' \n'.join(str(e) for e in family)
    subject = "Join the family on FamilyNotice"
    message = "You've been invited by " + request.user.first_name + " " + request.user.last_name + " to join FamilyNotice application.\nPlease visit FamilyNotice at http://localhost:8000/chooseFamily/ and use the respective key to join the family you would like to join.\n" + ListOfFamilies + "\nWe hope you enjoy your experience.\nBest, FamilyNotice Team"
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=email_arr, fail_silently=False)
    return redirect('choose family')

@csrf_exempt
def delete_task(request):
    try:
        value1 = list(request)
        stvalue = str(value1)
        splitValue = stvalue.split("'")
        Task_id = int(splitValue[1])
        instance = Task.objects.get(pk=Task_id)
        instance.delete()
        return JsonResponse({
            'response' : 'return response from delete member function',
            'taskID' : Task_id,
        })
    except:
        Http404(request)

def delete_chore(request):
    try:
        value1 = list(request)
        stvalue = str(value1)
        splitValue = stvalue.split("'")
        Chore_id = int(splitValue[1])
        instance = Chores.objects.get(pk=Chore_id)
        print(instance)
        instance.delete()
        return JsonResponse({
            'response' : 'return response from delete member function',
            'ChoreID' : Chore_id,
        })
    except:
        Http404(request)

def accept_claim(request):
        try:
            value1 = list(request)
            stvalue = str(value1)
            splitValue = stvalue.split("'")
            Claim_id = int(splitValue[1])
            instance = ClaimReward.objects.get(pk=Claim_id)
            print(instance)
            instance.delete()
            return JsonResponse({
                'response' : 'return response from delete member function',
                'ClaimID' : Claim_id,
            })
        except:
            return JsonResponse({
                'response' : 'FAIL',
            })


def delete_reward(request):
    try:
        value1 = list(request)
        stvalue = str(value1)
        splitValue = stvalue.split("'")
        RewardID = int(splitValue[1])
        instance = Rewards.objects.get(pk=RewardID)
        print(instance)
        instance.delete()
        return JsonResponse({
            'response' : 'return response from delete member function',
            'RewardID' : RewardID,
        })
    except:
        Http404(request)

def chore_completed(request):
    value1 = list(request)
    stvalue = str(value1)
    splitValue = stvalue.split("'")
    Chore_id = int(splitValue[1])
    instance = Chores.objects.get(pk=Chore_id)
    instance.completed = True
    members = Member.objects.filter(chores=Chore_id)
    for mem in members:
        print("Before: ", mem.points)
        mem.points = mem.points + instance.points
        mem.Currentpoints = mem.Currentpoints + instance.points
        print("After: ", mem.points)
        mem.save()
    instance.save()
    return JsonResponse({
        'response' : 'return response from complete chores',
    })

@login_required
def chores(request):
    try:
        family_session = request.session['family_session']
    except:
        return redirect('choose family')
    mem = Member.objects.get(user = request.user)
    familyfilter = Family.objects.get(nameofFamily = family_session)
    chorelist = ChoreList.objects.get(family=familyfilter)
    rewards = Rewards.objects.filter(chorelist = chorelist)
    ordered2 = rewards.order_by('pointsNeeded')
    rewards_serialize= json.loads(serialize('json', ordered2))
    if mem.userType == "FamilyMember":
        chores = Chores.objects.filter(assignChoreTo=mem)
        ordered = chores.order_by('-completed')
        chores_serialize= json.loads(serialize('json', ordered))
        mylist = zip(chores_serialize, ordered)
        claim = ClaimReward.objects.filter(member=mem)
        context ={
        'member' : mem,
        'chores' : mylist,
        'rewards' : rewards_serialize,
        'claim' : claim,
        }
        return render(request,'mainapp/choresKids.html' ,context)
    else:
        chores = Chores.objects.filter(chorelist = chorelist)
        claim = ClaimReward.objects.filter(chorelist = chorelist)
        ordered = chores.order_by('completed')
        chores_serialize= json.loads(serialize('json', ordered))
        mylist2 = zip(chores_serialize, ordered)
        context ={
        'member' : mem,
        'chores' : mylist2,
        'rewards' : rewards_serialize,
        'claim' : claim,
        }
        return render(request,'mainapp/choresGuardians.html' ,context)

def claim(request):
    try:
        family_session = request.session['family_session']
    except:
        return redirect('choose family')
    value1 = list(request)
    stvalue = str(value1)
    splitValue = stvalue.split("'")
    RewardID = int(splitValue[1])
    instance = Rewards.objects.get(pk=RewardID)
    print(instance)
    mem = Member.objects.get(user = request.user)
    points = mem.Currentpoints
    if(points >= instance.pointsNeeded):
        claim = ClaimReward(name = instance.name, member=request.user.first_name)
        claim.save()
        mem.Currentpoints = mem.Currentpoints - instance.pointsNeeded
        print("I GET HERE")
        mem.save()
        familyfilter = Family.objects.get(nameofFamily = family_session)
        chorelist = ChoreList.objects.get(family=familyfilter)
        chorelist.claim.add(claim)
        chorelist.save()
        return JsonResponse({
            'response' : 'CLAIMED',
        })
    else:
        return JsonResponse({
            'response' : 'YOU NEED MORE POINTS',
        })


@login_required
def todolist(request):
    try:
        family_session = request.session['family_session']
    except:
        return redirect('choose family')
    context = {
        'response' : 'You are in the index page',
    }

    return render(request,'mainapp/todolists.html' ,{})

@login_required
def meal_planner(request):
    try:
        family_session = request.session['family_session']
    except:
        return redirect('choose family')
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
        newMeal = MealDesc(description=desc, text=text)
        newMeal.save()
        try:
            family_session = request.session['family_session']
        except:
            return redirect('choose family')
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
    try:
        family_session = request.session['family_session']
    except:
        return redirect('choose family')
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
    try:
        family_session = request.session['family_session']
    except:
        return redirect('choose family')
    form = MealEntryForm()
    context = { 'form' : form, 'meal':meal,}
    print(meal)
    return render(request,'mainapp/newMeal.html', context)
