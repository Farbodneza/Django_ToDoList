from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from web.models import Task, Category
import random
import string

# Create your views here.]
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POSt.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if not username or password:
            messages.error(request, 'password and username needed!')
        elif User.objects.filter(username=username):
            messages.error(request, 'username already existed!')
        elif password != confirm_password:
            messages.error(request, 'password is not match!')
        else:
            User.objects.create_user(username=username, email=email, password=password)    
            messages.success(request, 'OK')
            redirect('login')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('tasks')
        messages.error(request, 'wrong password or username!')


@require_POST
@login_required
def logout(request):
    logout(request)
    return redirect("login")


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    categoriesd = Category.objects.filter(user=request.user)
    

@login_required
def creat_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        dead_line = request.POST.get('dead_line')

        if not title:
            messages.error(request, 'title needed!')
            return redirect('tasks')
        elif priority not in dict(Task.PRIORITY):
            messages(request, 'invalid priority!')
            return redirect('tasks')
        
        category = None
        if 'category' in request.POST:
            this_category=Category.objects.filter(name = request.POST['category'])
            if not this_category:
                Category.objects.create(
                    user=request.user,
                    name=request.POST['category'],
                )
                category=Category.objects.filter(name= request.POST['category']).get()
            else:
                category=Category.objects.filter(name = request.POST['category']).get()
        if 'dead_line' in request.POST:
            parse_date = parse_datetime(dead_line)
        else:
            parse_date= None
        
        Task.objects.create(
        user=request.user, 
        title=title,
        description=description,
        priority=priority,
        dead_line=parse_date,
        category=this_category,
        )

        messages.success(request, "Task created.")

@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        dead_line = request.POST.get('dead_line')

        if not title:
            messages.error(request, 'title needed!')
            return redirect('edit_task', pk=pk)
        elif priority not in dict(Task.PRIORITY):
            messages(request, 'invalid priority!')
            return redirect('edit_task', pk=pk)
        
        category = None
        if 'category' in request.POST:
            this_category=Category.objects.filter(name = request.POST['category'])
            if not this_category:
                Category.objects.create(
                    user=request.user,
                    name=request.POST['category'],
                )
                category=Category.objects.filter(name= request.POST['category']).get()
            else:
                category=Category.objects.filter(name = request.POST['category']).get()
        if 'dead_line' in request.POST:
            parse_date = parse_datetime(dead_line)
        else:
            parse_date= None
    
    task.title = title
    task.description = description
    task.priority = priority
    task.category = category
    task.dead_line = parse_date

    task.save()

    messages.success(request, 'Task updated!')

    return redirect(request, 'tasks')


@login_required
@require_POST
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()

    messages.success(request, 'Task deleted!')
    return redirect('tasks')


@login_required
@require_POST
def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_completed = not task.is_completed
    task.save()
    return redirect('tasks')


@login_required
def submit_category(request):
    Category.objects.create(
        user=request.user,
        name=request.POST['name'],
    )
    return redirect('tasks')

