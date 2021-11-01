from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login

# Create your views here.

def signupuser(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html',
                              {'form': UserCreationForm(), 'errmsg': 'That username has already been taken. '
                                                                     'Choose another one.'})
        else:
            return render(request, 'todo/signupuser.html',
                          {'form': UserCreationForm(), 'errmsg': 'Passwords didn\'t match.'})
    elif request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})

def currenttodos(request):
    return render(request, 'todo/currenttodos.html')
