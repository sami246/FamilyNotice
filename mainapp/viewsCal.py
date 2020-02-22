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
    # value1 = request.body
    # stvalue = str(value1)
    # splitValue = stvalue.split("'")
    # access_token = splitValue[1]
    success = request.body
    print(success)


    # Id = query.get('Id')
    # print(Id)
    # token = query.get('id_token')
    # expires_at = query.get('expires_at')
    # try:
    #     print('before id info')
    #     idinfo = id_token.verify_oauth2_token(token, requests.Request(), '451953960582-kfhho1v27s635d283hgi1ehhj7qte836.apps.googleusercontent.com')
    #     print('after id info')
    #     if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
    #         raise ValueError('Wrong issuer.')
    #     userid = idinfo['sub']
    #     print('VERIFIED')
    # except ValueError:
    #     print('FAILLLLLLLLLLL')
    #     pass
    return JsonResponse({
        'something' : 'something'
    })

def get_credentials(request):
    scopes = ['https://www.googleapis.com/auth/calendar']
    if request.session['result'] == 'false':
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes, redirect_uri='http://localhost:8000/calendar/')
        credentials = flow.run_local_server()
        print('#################')
        print(credentials)
        service = build("calendar", "v3", credentials=credentials)
        print('Service: ', service)
        result = service.calendarList().list().execute()
        request.session['result'] = result
    result = request.session['result']
    print('Result', result)
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
