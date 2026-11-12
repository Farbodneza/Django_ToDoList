from django.urls import path
from . import views


urlpatterns = [
    path('', views.task_list, name='tasks'),
    path('register/', views.register, name="register"),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('task/creat/', views.creat_task, name='creat_task'),
    path('task/edit/<int:pk>/', views.edit_task, name='edit_task'),
    path('task/delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('task/toggle/<int:pk>/', views.toggle_task, name='toggle_task'),
    path('category/create/', views.submit_category, name='submit_category'),
]