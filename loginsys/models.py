# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from lots.models import *
# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User)
    balance = models.IntegerField(null=False, default=0)
    avatarka = models.ImageField(upload_to='pictures', verbose_name='Аватарка', blank=True, null=False,default="pictures/not_ava.png")
