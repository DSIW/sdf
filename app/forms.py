from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from .models import Book

class NewBookForm(forms.ModelForm):
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
        if formset.is_valid():
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