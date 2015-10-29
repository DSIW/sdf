# coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Book

class BookForm(forms.ModelForm):
    '''
    Klasse zum erstellen der Buch Form
    widgets: Defintion wie die Eingabefelder auszusehen haben. Hier am Beispiel css Klasse von Bootstrap genutzt und Vorschau eingebaut
    labels: Definition was bei den Label Tags auf der Oberflaeche erscheinen soll. Wenn dies nicht definiert worde ist wird der Attributenname der Modellklasse genommen
    '''
    class Meta:
        LANGUAGES = (
            ('DE', _("Deutsch")),
            ('EN', _("Englisch")),
            ('FR', _("Französisch")),
            ('SP', _("Spanisch")),
        )
        model = Book
        exclude = ['Id', 'user']
        widgets = {
            'language': forms.Select(choices=LANGUAGES),
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


class RegistrationForm(UserCreationForm):
    first_name = forms.TextInput()
    last_name = forms.TextInput()

    paypal = forms.EmailInput()
    email = forms.EmailInput()

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','first_name', 'last_name', 'email','paypal', 'password1', 'password1')


    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.paypal = self.cleaned_data['paypal']

        if commit:
            user.save()
