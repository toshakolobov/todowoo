from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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


@login_required
def currenttasks(request):
    tasks = Task.objects.filter(user=request.user, completion_date__isnull=True)
    return render(request, 'todo/currenttasks.html', {'tasks': tasks})

@login_required
def completedtasks(request):
    tasks = Task.objects.filter(user=request.user, completion_date__isnull=False).order_by('-completion_date')
    return render(request, 'todo/completedtasks.html', {'tasks': tasks})

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
            return redirect('currenttasks')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')

@login_required
def createtask(request):
    if request.method == 'GET':
        return render(request, 'todo/createtask.html', {'form': TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('currenttasks')
        except ValueError:
            return render(request, 'todo/createtask.html', {'form': TaskForm, 'errmsg': 'Bad data. Try again.'})

@login_required
def viewtask(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'todo/viewtask.html', {'task': task, 'form': form})
    else:
        form = None
        try:
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('currenttasks')
        except ValueError:
            return render(request, 'todo/viewtask.html', {'task': task, 'form': form, 'errmsg': 'Bad data. Try again.'})

@login_required
def completetask(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if request.method == 'POST':
        task.completion_date = timezone.now()
        task.save()
        return redirect('currenttasks')

@login_required
def deletetask(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('currenttasks')
