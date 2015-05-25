# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import auth
class Lot(models.Model):
    Name = models.CharField(max_length=50, verbose_name = 'Назва')
    Description = models.TextField(verbose_name = 'Опис')
    FonPicture = models.ImageField(upload_to='pictures', verbose_name='Зображення', blank=True, null=False,default="pictures/not_image.png")
    pub_date = models.DateTimeField(null=False,verbose_name = 'Дата публікації', default = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
    min_price = models.IntegerField(verbose_name = 'Початкова ціна')
    min_stage = models.IntegerField(verbose_name = 'Мінімальний крок')
    user = models.ForeignKey(User)
    type_lot = models.IntegerField()
    def __str__(self):
        return self.Lot

class Comment(models.Model):
    lot = models.ForeignKey(Lot)
    text = models.TextField(verbose_name="Текст коментара")
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField()
    def __unicode__(self):
        return self.Comment
    # Create your models here.

class Registration(models.Model):
    lot_id = models.IntegerField()
    user = models.IntegerField()

class Like(models.Model):
    lot_id = models.IntegerField()
    user = models.IntegerField()

class Rate(models.Model):
    price = models.IntegerField()
    lot = models.ForeignKey(Lot)
    user = models.ForeignKey(User)
    date_rate = models.DateTimeField(null=False,verbose_name = 'Дата ставки', default = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
