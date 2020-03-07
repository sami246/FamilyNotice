from django import forms
from .enums import *
from .models import *
from django.contrib.auth.models import User

class MealEntryForm(forms.ModelForm):
    class Meta:
        model = MealDesc
        fields = ('text', 'description')
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder' : "Name of Meal",
                'class' : 'form-control',
            }),
            'description' : forms.Textarea(attrs={
                'placeholder' : "Description of Meal",
                'class' : 'form-control',
                'rows':10,
            })
        }

class RewardForm(forms.ModelForm):
    class Meta:
        model = Rewards
        fields = ('name', 'pointsNeeded')
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder' : "Name of Reward",
                'class' : 'form-control',
            }),
            'pointsNeeded': forms.NumberInput(attrs={
                'placeholder' : "Points",
                'class' : 'form-control',
            }),
        }

class ChoreForm(forms.ModelForm):
    class Meta:
        model = Chores
        fields = ('name', 'points', 'description', 'dueBy', 'assignChoreTo',)
        # assignChoreTo = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
        widgets = {
            'assignChoreTo': forms.CheckboxSelectMultiple(attrs={
                # 'class' : 'form-control',
                # 'style' : 'display:inline;'
            }),
            'name': forms.TextInput(attrs={
                'placeholder' : "Name of Chore",
                'class' : 'form-control',
            }),
            'points': forms.NumberInput(attrs={
                'placeholder' : "Points",
                'class' : 'form-control',
            }),
            'description' : forms.Textarea(attrs={
                'placeholder' : "Description of Chore",
                'class' : 'form-control',
                'rows':3,
            }),
            'dueBy' : forms.TextInput(attrs={
                'placeholder' : 'YYYY-MM-DD HH:MM:SS',
                'class' : 'form-control',
            }),
        }
        labels = {
            'dueBy': ('End time (YYYY-MM-DD HH:MM:SS)'),
        }

        # def __init__(self, *args, **kwargs):
        #     super(ChoreForm, self).__init__(*args, **kwargs)
        #     family  = request.session['family_session']
        #     self.fields['assignChoreTo'].queryset = Member.objects.filter(family=family)

class CalendarForm(forms.ModelForm):
    class Meta:
        model = EventEntry
        fields = ('summary','description', 'location', 'duration', 'start_time')
        widgets = {
            'summary': forms.TextInput(attrs={
                'placeholder' : "Title of New Event",
                'class' : 'form-control',
            }),
            'location': forms.TextInput(attrs={
                'placeholder' : "Location",
                'class' : 'form-control',
            }),
            'duration': forms.NumberInput(attrs={
                'placeholder' : "Number",
                'class' : 'form-control',
            }),
            'description' : forms.Textarea(attrs={
                'placeholder' : "Description of Event",
                'class' : 'form-control',
                'rows':5,
            }),
            'start_time': forms.TextInput(attrs={
                'placeholder' : "Start Time",
                'class' : 'form-control',
            }),

        }
        help_texts = {
            'duration': 'Time Event will last in hours',
            'start_time' : 'E.g 29th February 3pm'
        }


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ('nameOfList',)
        widgets = {
            'nameOfList': forms.TextInput(attrs={
                'placeholder' : "Name of new List",
                'class' : 'form-control',
            })
        }

class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ('nameofFamily', 'members')
        widgets = {
            'nameofFamily': forms.TextInput(attrs={
                'placeholder' : "Name of New Family",
                'class' : 'form-control',
            }),
            'members' : forms.SelectMultiple(attrs={
                'class' : 'form-control',
            })
        }
