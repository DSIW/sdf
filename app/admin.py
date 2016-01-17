# -*- coding: utf-8 -*-

from django.contrib import admin

# Register your models here.
from .models import FAQ


class FAQAdmin(admin.ModelAdmin):
    exclude = ('createdAt','updatedAt',)

admin.site.register(FAQ,FAQAdmin)
