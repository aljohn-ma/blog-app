import datetime

from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    title = models.CharField(max_length=500,default='')
    content = models.TextField(null=False,default='')
    cover_image = models.FileField(upload_to='documents/')
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title