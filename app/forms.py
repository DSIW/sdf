# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import StaticPage

from .models import FAQ,  StaticPage


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        exclude = ['author','createdAt','updatedAt']

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

