# -*- coding: utf-8 -*-

from django.db import models
from app_user.models import User

from datetime import datetime

class FAQ(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    position = models.IntegerField()
    createdAt = models.DateField('created_at')
    updatedAt = models.DateField('updated_at')
    author = models.ForeignKey(User,default=None)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
        return super(FAQ, self).save(*args, **kwargs)



class StaticPage(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.name + ", " + self.title + " (" + self.content + ")"
