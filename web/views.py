from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from web.models import User, Token, Task, Category
# Create your views here.]
@csrf_exempt
def submit_category(request):
    this_token = request.POST['token']
    this_user = User.objects.filter(token__token = this_token).get()
    Category.objects.create(
        user=this_user,
        name=request.POST['name'],
    )
    return JsonResponse({
        'status': 'ok',
    }, encoder=json.JSONEncoder)



@csrf_exempt
def submit_task(request):
    this_token = request.POST['token']
    this_user = User.objects.filter(token__token = this_token).get()
    if 'dead_line' in request.POST:
        user_dead_line=request.POST['dead_line']
    else:
        user_dead_line= None
    if 'category' in request.POST:
        this_category=Category.objects.filter(name = request.POST['category'])
        if not this_category:
            Category.objects.create(
                user=this_user,
                name=request.POST['category'],
            )
            this_category=Category.objects.filter(name= request.POST['category']).get()
        else:
            this_category=Category.objects.filter(name = request.POST['category']).get()

    
    else:
        this_category= None

    Task.objects.create(
        user=this_user, 
        title=request.POST['title'],
        description=request.POST['description'],
        priority=request.POST['priority'],
        dead_line=user_dead_line,
        category=this_category,
        )
    return JsonResponse({
        'status': 'ok',
    }, encoder=json.JSONEncoder)