# -*- coding: utf-8 -*-

from django.db import models

class StaticPage(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.name + ", " + self.title + " (" + self.content + ")"
