# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models  import User as AuthUser
# Register your models here.


class ShowCaseAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('user_ptr','username','password','first_name','last_name','email')
        }),
        ('Erweitert', {
            'classes': ('collapse',),
            'fields': ('emailConfirm','showcaseDisabled')
        }),
        ('System', {
            'classes': ('collapse',),
            'fields': ('groups','is_staff','is_active','date_joined','last_login','is_superuser')
        }),
    )

admin.site.unregister(AuthUser)
admin.site.register(User, ShowCaseAdmin)
