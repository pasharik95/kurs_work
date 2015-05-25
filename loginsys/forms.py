__author__ = 'Pasha'
from django.test import TestCase
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from models import *
from django.contrib.auth.forms import UserCreationForm

class RegUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2','first_name','last_name','email']
class EditProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['avatarka']