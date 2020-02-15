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

def get_credentials(request):
    scopes = ['https://www.googleapis.com/auth/calendar']
    try:
        credentials = pickle.load(open("token.pkl", "rb"))
    except:
        credentials = ""
    if not credentials:
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
        credentials = flow.run_console()
        pickle.dump(credentials, open("token.pkl", "wb"))
    print('CRED')
    print(credentials)
    service = build("calendar", "v3", credentials=credentials)
    result = service.calendarList().list().execute()
    numofcalendars = len(result['items'])
    calArrID = [0] * numofcalendars
    calArrCol = [0] * numofcalendars
    #API doesn't work if calendar asked for is contacts because it is not sharable, therefore get rid of it
    for i in range(0, numofcalendars, 1):
        if result['items'][i]['id'] == "addressbook#contacts@group.v.calendar.google.com":
            calArrID[i] = calArrID[i-1]
        else:
            calArrID[i] = result['items'][i]['id']
    calendar_id = result['items'][0]['id']
    result2 = service.events().list(calendarId=calendar_id).execute()

    # create_event('25 Feb 12.30pm', service, "Test Meeting using CreateFunction Method",0.5,"dkalpa@email.com.au","Test Description","Mentone, VIC,Australia")
    return render(request,'mainapp/calendar.html' ,{'response' : result, 'calArr':calArrID})


def create_event(start_time_str, service, summary, duration=1,attendees=None, description=None, location=None):
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
            'timeZone': "GMT+00:00"
        },
        'attendees': [
        {'email':attendees },
    ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    print('''*** %r event added:
    With: %s
    Start: %s
    End:   %s''' % (summary.encode('utf-8'),
        attendees,start_time, end_time))

    return service.events().insert(calendarId='primary', body=event,sendNotifications=True).execute()
