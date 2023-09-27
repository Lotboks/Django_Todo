from django.db import models
from django.contrib.auth.models import User

class TaskContainer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Task(models.Model):
    container = models.ForeignKey(TaskContainer, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(default='', blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    due = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    def __str__(self):  
        return self.title
    
    
