from django.forms import ModelForm, fields
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class CreateUserForm(UserCreationForm):
    mob = forms.IntegerField()
    age = forms.IntegerField()
    class Meta:
        model = User
        fields = ['username', 'email', 'mob', 'age', 'password1', 'password2',]
        labels = {'mob' : 'Mobile Number', 'age': 'Age'}
        
