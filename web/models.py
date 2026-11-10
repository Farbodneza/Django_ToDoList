from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name

class Task(models.Model):
    PRIORITY = {
        'L': 'Low',
        'M': 'Medium',
        'H': 'High',
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=1, choices=PRIORITY)
    dead_line = models.DateTimeField(null=True, blank=True)
    creat_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks',)
    
    def __str__(self):
        return self.title
    def __unicode__(self):
        return "{}-{}".format(self.category, self.title)