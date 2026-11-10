from django.urls import path
from . import views


urlpatterns = [
    path('submit/task/', views.submit_task, name='submit_task'),
    path('submit/category/', views.submit_category, name='submit_category')
]