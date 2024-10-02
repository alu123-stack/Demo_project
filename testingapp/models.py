from typing import Any
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class TaskModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_delete = False)
    
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    createdd_at=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_task")
    completed= models.BooleanField(default=False)
    is_delete = models.BooleanField(default = False)

    objects = TaskModelManager()
    admin_objects = models.Manager()


    def __str__(self):
        return self.title
        
