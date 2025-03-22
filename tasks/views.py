from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm, RegisterForm

# User Authentication Views
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task-list')  # Redirect to task list after registration
    else:
        form = RegisterForm()
    return render(request, 'tasks/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('task-list')  # Redirect to task list after login
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

# Task Management Views
@login_required
def task_list(request):
    query = request.GET.get('q')
    status_filter = request.GET.get('status')
    tasks = Task.objects.filter(user=request.user)

    if query:
        tasks = tasks.filter(title__icontains=query)
    if status_filter in ['pending', 'completed']:
        tasks = tasks.filter(status=status_filter)

    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Assign the current user to the task
            task.save()
            return redirect('task-list')  # Redirect to the task list after saving the task
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('task-list')  # Redirect to task list after deleting the task
