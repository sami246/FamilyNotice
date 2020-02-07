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
