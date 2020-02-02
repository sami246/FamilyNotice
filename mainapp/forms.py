from django import forms
from .enums import *
from .models import *
from django.contrib.auth.models import User

class MealEntryForm(forms.ModelForm):
    class Meta:
        model = MealDesc
        fields = ('text', 'description')
