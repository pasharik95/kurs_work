# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from forms import *

# Create your views here.
def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST :
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            print(auth.get_user(request).username)
            return redirect('/')
        else:
            args['login_error'] = "error"
            return render_to_response('login.html', args)
    else:
        return render_to_response('login.html', args)

def logout(request):
    auth.logout(request)
    return redirect('/')

def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = RegUserForm()
    args['name_form'] = 'Зареєструватися'
    if request.POST:
        newuser_form = RegUserForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username = newuser_form.cleaned_data['username'], password = newuser_form.cleaned_data['password1'])
            auth.login(request, newuser)
            profile = Profile()
            profile.user = newuser
            profile.save()
            return redirect('/')
        else:
            args['form'] = newuser_form


    return render_to_response('register.html', args)

def editprofile(request):
    context = {}
    context.update(csrf(request))
    user = auth.get_user(request)
    context['user'] = user
    context['name_form'] = 'Зберегти'
    try:
        user = auth.get_user(request)
        if type(user) != AnonymousUser:
            profile = Profile.objects.get(user=user)
            form = EditProfileForm()
            if request.POST:
                print request.FILES
                form = EditProfileForm(request.POST, request.FILES)

                if form.is_valid():
                    print 11111
                    profileT = form.save(commit=False)
                    print profileT.avatarka
                    profile.avatarka = profileT.avatarka
                    profile.save()
                else:
                    context['form'] = form
                    return render_to_response('editprofile.html', context)

                return redirect('/')
            context['form'] = form
            if user.username == profile.user.username:
                form = EditProfileForm(instance = profile)
                context['form'] = form

            return render_to_response('editprofile.html', context)
    except ObjectDoesNotExist:
        pass

    return redirect('/')