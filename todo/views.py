from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from todo.forms import TaskForm

# Create your views here.


def homepage(request):
    return render(request, 'todo/homepage.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
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


def currenttodos(request):
    return render(request, 'todo/currenttodos.html')

def signinuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signinuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/signinuser.html', {'form': AuthenticationForm(),
                                                            'errmsg': 'Username or password didn\'t match.'})
        else:
            login(request, user)
            return redirect('currenttodos')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')

def createtask(request):
    if request.method == 'GET':
        return render(request, 'todo/createtask.html', {'form': TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtask.html', {'form': TaskForm, 'errmsg': 'Bad data. Try again.'})