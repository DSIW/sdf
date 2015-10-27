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
        model = Book
        exclude = ['Id', 'isOnStoreWindow']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'releaseDate': forms.DateInput(attrs={'class': 'form-control datepicker', 'data-provide': 'datepicker'}),
            'pageNumber': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn10': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn13': forms.TextInput(attrs={'class': 'form-control'}),
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
