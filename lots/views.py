# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect, render
from django.contrib import auth
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from django.core.context_processors import csrf
from lots.models import *
from forms import *
from  loginsys.models import Profile
import datetime
from django.contrib.auth.models import AnonymousUser
# Create your views here.
from django.http import HttpResponse



def lots(request):

    context = {}
    context['lots'] = Lot.objects.filter(type_lot__in = [0, 1, 2])
    if auth.get_user(request).username:
        context['user'] = auth.get_user(request)
        profile =  Profile.objects.get(user = auth.get_user(request).id)
        context['profile'] = profile
    return render_to_response('lots.html', context)

def lot(request, lot_id=1):

    context = {}
    context.update(csrf(request))
    lot = Lot.objects.get(id = lot_id)

    context['user'] = auth.get_user(request)
    context['lot'] = lot
    like = Like.objects.filter(lot_id = lot_id)
    i = 0
    for one_like in like:
        i += 1
    context['like_count'] = i
    context['comments'] = Comment.objects.filter(lot = lot_id)
    context['rates'] = Rate.objects.filter(lot = lot_id)
    context['now_price'] = lot.min_price
    rate = Rate.objects.filter(lot = lot_id)
    if rate:
        rate = rate.order_by("price").reverse()
        context['now_price'] = rate[0].price
        lot.min_price = rate[0].price
        lot.save()
        print(lot.min_price)
    if auth.get_user(request).username:
        context['form'] = CommentForm()
    reg_user = Registration.objects.filter(lot_id = lot_id).filter(user = auth.get_user(request).id)
    context['reg_r'] = True
    if reg_user and lot.type_lot == 0 :
        context['reg_r'] = False
    if reg_user and lot.type_lot == 2 :
        context['rate_form'] = RateForm()
        context['reg'] = True
    return render_to_response('lot.html', context)

def newlot(request):
    context = {}
    context.update(csrf(request))
    context['form'] = LotForm()
    context['name_form'] = 'Новий лот'
    context['user'] = auth.get_user(request)
    form = LotForm()
    if request.POST:
        form = LotForm(request.POST, request.FILES)
        if form.is_valid():
            lot = form.save(commit=False)
            lot.pub_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
            lot.type_lot = 0
            lot.user = auth.get_user(request)
            form.save()
            change_of_state(lot.id)
            return redirect('/')
    return render_to_response('new.html', context)
def delete(request, lot_id):
    try:
        lot = Lot.objects.get(id=lot_id)
        user = auth.get_user(request)
        if user.username == lot.user.username:
            for com in Comment.objects.filter(lot_id=lot.id):
                com.delete()
            for l in Like.objects.filter(lot_id=lot.id).filter(user = auth.get_user(request).id):
                l.delete()
            lot.delete()
    except ObjectDoesNotExist:
        pass

    return redirect('/')
def editA(request, lot_id):
    context = {}
    context.update(csrf(request))
    context['user'] = auth.get_user(request)
    context['name_form'] = 'Редагувати'
    try:
        user = auth.get_user(request)
        if type(user) != AnonymousUser:
            lot = Lot.objects.get(id=lot_id)
            form = LotEditForm()
            if request.POST:
                form = LotEditForm(request.POST, request.FILES)

                if form.is_valid():
                    lotT = form.save(commit=False)
                    lot.Name = lotT.Name
                    lot.Description = lotT.Description
                    lot.min_price = lotT.min_price
                    lot.min_stage = lotT.min_stage
                    lot.save()
                else:
                    context['form'] = form
                    return render_to_response('new.html', context)

                return redirect('/')
            context['form'] = form
            if user.username == lot.user.username:
                form = LotEditForm(instance = lot)
                context['form'] = form

            return render_to_response('new.html', context)
    except ObjectDoesNotExist:
        pass

    return redirect('/')
def addlike(request, lot_id):
    try:
        lot = Lot.objects.get(id = lot_id)
        one_like = Like.objects.filter(lot_id = lot_id).filter(user = auth.get_user(request).id)
        if one_like:
            #delete
            one_like.delete();
        else:
            #add
            one_like = Like()
            one_like.user = auth.get_user(request).id
            one_like.lot_id = lot_id
            one_like.save()
        lot.save()
    except ObjectDoesNotExist:
         raise Http404
    return redirect('/lots/get/%s/'% lot_id)
def registration_on_lot(request, lot_id):
    lot = Lot.objects.get(id = lot_id)
    if lot.type_lot == 0:
        reg = Registration()
        reg.user = auth.get_user(request).id
        reg.lot_id = lot_id
        reg.save()
    return redirect('/lots/get/' + str(lot_id) + '/')

def addcomment(request, lot_id):
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.lot = Lot.objects.get(id = lot_id)
            comment.pub_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
            comment.user = auth.get_user(request)
            form.save()
    return redirect('/lots/get/%s/'% lot_id)
def addmoney(request):
    profile = Profile.objects.get(user = auth.get_user(request))
    print (profile)
    if profile:
        profile.balance += 200
        profile.save()
    return redirect('/')
def mylots(request):
    context = {}
    context['user'] = auth.get_user(request)
    profile =  Profile.objects.get(user = auth.get_user(request).id)
    context['profile'] = profile
    lots = Lot.objects.filter(user = auth.get_user(request))
    if lots:
         context['lots'] = lots
    return render_to_response('lots.html', context)
def change_of_state(lot_id):
    lot = Lot.objects.get(id = lot_id)
    datetime_wait_start = datetime.datetime.now() + datetime.timedelta(minutes=1)
    datetime_start = datetime_wait_start + datetime.timedelta(minutes=1)
    datetime_end = datetime_start + datetime.timedelta(minutes=1)

    strName = 'AddedInfo' + str(lot.id)
    querry = 'CREATE EVENT {0} ' \
                     'ON SCHEDULE ' \
                     'AT \'{1}\' ' \
                     'ON COMPLETION NOT PRESERVE ' \
                     'DO ' \
                     'UPDATE kursdb.lots_lot SET lots_lot.type_lot = 1 WHERE id = {2};'.format(strName + 'wait_start', datetime.datetime.strftime(datetime_wait_start, "%Y-%m-%d %H:%M:%S"), lot_id)

    querry1 = 'CREATE EVENT {0} ' \
                     'ON SCHEDULE ' \
                     'AT \'{1}\' ' \
                     'ON COMPLETION NOT PRESERVE ' \
                     'DO ' \
                     'UPDATE kursdb.lots_lot SET lots_lot.type_lot = 2 WHERE id = {2};'.format(strName + 'start', datetime.datetime.strftime(datetime_start, "%Y-%m-%d %H:%M:%S"), lot_id)
    querry2 = 'CREATE EVENT {0} ' \
                     'ON SCHEDULE ' \
                     'AT \'{1}\' ' \
                     'ON COMPLETION NOT PRESERVE ' \
                     'DO ' \
                     'UPDATE kursdb.lots_lot SET lots_lot.type_lot = 3 WHERE id = {2};'.format(strName + 'end', datetime.datetime.strftime(datetime_end, "%Y-%m-%d %H:%M:%S"), lot_id )

    connection.cursor().execute(querry)
    connection.cursor().execute(querry1)
    connection.cursor().execute(querry2)
def myshopping(request):
    context = {}
    context['user'] = auth.get_user(request)
    profile =  Profile.objects.get(user = auth.get_user(request).id)
    numbers_lots = []
    lots = Lot.objects.filter(user = auth.get_user(request))
    context['profile'] = profile
    lots = Lot.objects.filter(type_lot = 3)
    for lot in lots:
        rates = Rate.objects.filter(lot = lot)
        if rates:
            rates = rates.order_by("price").reverse()
            if rates[0].user == auth.get_user(request):
                numbers_lots.append(rates[0].lot)

    if lots:
         context['lots'] = numbers_lots
    return render_to_response('lots.html', context)
def myrates(request):
    context = {}
    context['user'] = auth.get_user(request)
    profile =  Profile.objects.get(user = auth.get_user(request).id)
    numbers_lots = []
    context['profile'] = profile
    rates = Rate.objects.filter(user = auth.get_user(request).id)
    for rate in rates:
        if numbers_lots.count(rate.lot) == 0:
            numbers_lots.append(rate.lot)

    if numbers_lots:
         context['lots'] = numbers_lots
    return render_to_response('lots.html', context)
def statistics(request):
    context = {}
    context['user'] = auth.get_user(request)
    #виграно
    lots = Lot.objects.filter(type_lot = 3)
    x1 = 0
    for lot in lots:
        rates = Rate.objects.filter(lot = lot)
        if rates:
            rates = rates.order_by("price").reverse()
            if rates[0].user == auth.get_user(request):
                x1 += 1
    #ставок
    x2 = 0
    numbers_lots = []
    rates = Rate.objects.filter(user = auth.get_user(request).id)
    for rate in rates:
        if numbers_lots.count(rate.lot) == 0:
            numbers_lots.append(rate.lot)
            x2 += 1
    context['x1'] = x1
    context['x2'] = x2
    if auth.get_user(request).username:
        context['user'] = auth.get_user(request)
        profile =  Profile.objects.get(user = auth.get_user(request).id)
        context['profile'] = profile
    return render_to_response('statistics.html', context)
def addrate(request, lot_id):
    profile = Profile.objects.get(user = auth.get_user(request))
    if request.POST:
        lot = Lot.objects.get(id = lot_id)
        form = RateForm(request.POST)
        comment = form.save(commit=False)
        rate = Rate.objects.filter(lot = lot_id)
        if form.is_valid():
            if rate:
                rate = rate.order_by("price").reverse()
                profile = Profile.objects.get(user = rate[0].user)
                profile.balance += rate[0].price
                profile.save()
            if (lot.min_stage +  lot.min_price)<= comment.price and profile.balance >= comment.price:
                profile.balance -= comment.price
                profile.save()
                comment.lot = Lot.objects.get(id = lot_id)
                comment.pub_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
                comment.user = auth.get_user(request)
                form.save()
    return redirect('/lots/get/%s/'% lot_id)






