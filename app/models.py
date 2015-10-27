# coding=utf-8
from django.db import models

# Create your models here.
class Book(models.Model):
    name= models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    language = models.CharField(max_length=100)
    releaseDate = models.DateTimeField('release_date')
    pageNumber = models.IntegerField(default=1)
    isbn10 = models.CharField(max_length=100)
    isbn13 = models.CharField(max_length=100)
    isOnStoreWindow = models.BooleanField(default=False)
