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
import pickle
import datefinder
import timedelta
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import id_token
from google.auth.transport import requests


def cal_user(request):
    return JsonResponse({
        'something' : 'something'
    })

def get_credentials(request):
    try:
        family_session = request.session['family_session']
    except:
        return redirect('choose family')
    fam = Family.objects.get(nameofFamily = family_session)

    scopes = ['https://www.googleapis.com/auth/calendar']

    #Crentials for Family Calendar
    credentialsDanu = pickle.load(open("token.pkl", "rb"))
    serviceDanu = build("calendar", "v3", credentials=credentialsDanu)
    if fam.cal == False:
        summary = fam.nameofFamily + " Family Calendar"
        calendar = {
        'summary': summary,
        }
        created_calendar = serviceDanu.calendars().insert(body=calendar).execute()
        fam.cal = True
        fam.calId = created_calendar['id']
        fam.save()

    #Crentials for Personal Calendar
    if request.session['result'] == 'false':
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes, redirect_uri='http://localhost:8000/calendar/')
        credentials = flow.run_local_server()
        service = build("calendar", "v3", credentials=credentials)
        result = service.calendarList().list().execute()
        request.session['result'] = result
    result = request.session['result']

    #Getting all public calendars from personal Calendar
    numofcalendars = len(result['items'])
    calArrID = [0] * (int(numofcalendars))
    calArrCol = [0] * (int(numofcalendars))
    #API doesn't work if calendar asked for is contacts because it is not sharable, therefore get rid of it
    for i in range(0, numofcalendars, 1):
        # if result['items'][i]['id'] == "addressbook#contacts@group.v.calendar.google.com":
        if "group.v.calendar.google.com" in result['items'][i]['id']:
            calArrID[i] = calArrID[0]
        else:
            calArrID[i] = result['items'][i]['id']
    calendar_id = result['items'][0]['id']


    # create_event2('28 Feb 2.30pm', serviceDanu, "Test",0.5,"dkalpa@email.com.au","Test Description","Mentone, VIC,Australia")
    form = CalendarForm()
    context = {
    'response' : result,
    'calArr':calArrID,
    'Famcalendar' : fam.calId,
    'form' : form
    }
    return render(request,'mainapp/calendar.html' ,context)

def SignOutGoogle(request):
    request.session['result'] = 'false'
    return redirect('calendar')


def create_event(request):
    family_session = request.session['family_session']
    fam = Family.objects.get(nameofFamily = family_session)
    credentialsDanu = pickle.load(open("token.pkl", "rb"))
    serviceDanu = build("calendar", "v3", credentials=credentialsDanu)
    scopes = ['https://www.googleapis.com/auth/calendar']

    start_time_str = request.POST['start_time']
    summary = request.POST['summary']
    duration = int(request.POST['duration'])
    description = request.POST['description']
    location = request.POST['location']

    matches = list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta.Timedelta(hours=duration)

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': "GMT+00:00",
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            # 'dateTime': end_time,
            'timeZone': "GMT+00:00"
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    created = serviceDanu.events().insert(calendarId=fam.calId, body=event).execute()
    print('CREATED :', created)
    event = EventEntry(
        summary = summary,
    	description = description,
    	location = location,
    	start_time = start_time_str,
    	duration = duration,
    )
    event.save()
    fam.calEvents.add(event)
    return redirect('calendar')
