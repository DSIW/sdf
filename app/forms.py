# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import StaticPage

class StaticPageForm(forms.ModelForm):
    '''
    Klasse zum erstellen der StaticPage Form
     '''
    class Meta:
        model = StaticPage
        exclude = ['name']
        widgets = {}
        labels = {
            'title': _('Titel'),
            'content': _('Inhalt'),
        }

