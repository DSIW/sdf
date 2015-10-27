# coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from .models import Book

class BookForm(forms.ModelForm):
    '''
    Klasse zum erstellen der Buch Form
    widgets: Defintion wie die Eingabefelder auszusehen haben. Hier am Beispiel css Klasse von Bootstrap genutzt und Vorschau eingebaut
    labels: Definition was bei den Label Tags auf der Oberflaeche erscheinen soll. Wenn dies nicht definiert worde ist wird der Attributenname der Modellklasse genommen
    '''
    class Meta:
        GENDER = (
            ('DE', _("Deutsch")),
            ('EN', _("Englisch")),
            ('FR', _("Französisch")),
            ('SP', _("Spanisch")),
        )
        model = Book
        exclude = ['Id', 'isOnStoreWindow']
        widgets = {
            'language': forms.Select(choices=GENDER),
            'releaseDate': forms.DateInput(attrs={'class': 'datepicker'}),
        }
        labels = {
            'name': _('Buchname'),
            'author': _('Author'),
            'language': _('Sprache'),
            'releaseDate': _('Veröffentlichungsdatum'),
            'pageNumber': _('Seitenanzahl'),
            'isbn10': _('ISBN-10'),
            'isbn13': _('ISBN-13'),
        }
