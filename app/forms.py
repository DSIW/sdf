from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from .models import Book

class NewBookForm(forms.ModelForm):
    '''
    Klasse zum erstellen der Buch Form
    widgets: Defintion wie die Eingabefelder auszusehen haben. Hier am Beispiel css Klasse von Bootstrap genutzt und Vorschau eingebaut
    labels: Definition was bei den Label Tags auf der Oberflaeche erscheinen soll. Wenn dies nicht definiert worde ist wird der Attributenname der Modellklasse genommen
    '''
    class Meta:
        model = Book
        exclude = ['Id', 'isOnStoreWindow']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buchname'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Author des Buches'}),
            'language': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sprache des Buches'}),
            'releaseDate': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Veröffentlichungsdatum', 'data-date-format': 'dd.mm yyyy', 'data-provide': 'datepicker'}),
            'pageNumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seitenzahl'}),
            'isbn10': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ISBN-10 Nummer'}),
            'isbn13': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ISBN-13 Nummer'}),
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

    def validateAndSaveNewBook(formset):
        '''
        Diese Methode prueft ob die Eingaben alle erfolgreich waren is_valid(). Danach wird geprueft ob ueberhaupt Eingaben gemacht worden sind.
        Wenn alles erfolgreich war wird das neue Buch gespeichert
        :param formset: Buch Form
        :return: None
        '''
        if formset.is_valid():
            ''' Pruefe ob Benutzer ueberhaupt Eingaben gemacht hat '''
            is_really_valid = True
            for form in formset.forms:
                if not 'name' in form.cleaned_data:
                    is_really_valid = False
                    break

            if(is_really_valid):
                formset.save()
            else:
                raise ValidationError("Es gab leere Eingabefelder")
        else:
            raise ValidationError("Eingabefelder waren nicht valide")

    def validateAndUpateBook(form):
        '''Diese Methode wird zum aktulaisieren eines Buches genutzt
        '''
        if form.is_valid():
            is_really_valid = True
            if not 'name' in form.cleaned_data:
                is_really_valid = False
            if(is_really_valid):
                form.save()
            else:
                raise ValidationError("Es gab leere Eingabefelder")
        else:
            raise ValidationError("Eingabefelder waren nicht valide")
