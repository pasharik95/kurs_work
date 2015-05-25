from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from models import *
class LotForm(ModelForm):
    class Meta:
        model = Lot
        fields = ['Name', 'Description','FonPicture', 'min_price', 'min_stage']

class LotEditForm(ModelForm):
    class Meta:
        model = Lot
        fields = ['Name', 'Description', 'min_price', 'min_stage']
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class LikeForm(ModelForm):
    class Meta:
        model = Like

class RateForm(ModelForm):
    class Meta:
        model = Rate
        fields = ['price']
