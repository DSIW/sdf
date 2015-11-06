# coding=utf-8
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.forms.utils import ErrorDict

from .models import User, Book, Offer


class OfferForm(forms.ModelForm):
    offer_form_checkbox = forms.BooleanField(label=_('Verkaufen'))

    class Meta:
        model = Offer
        fields = ['offer_form_checkbox', 'price', 'shipping_price']
        exclude = ['id', 'book', 'seller_user']
        labels = {
            'price': _('Buchpreis'),
            'shipping_price': _('Versandpreis'),
        }

    # Returns errors only if user has actually changed the form
    def full_clean(self):
        if not self.has_changed():
            self._errors = ErrorDict()
            return

        return super(OfferForm, self).full_clean()


class BookForm(forms.ModelForm):
    '''
    Klasse zum erstellen der Buch Form
    widgets: Defintion wie die Eingabefelder auszusehen haben. Hier am Beispiel css Klasse von Bootstrap genutzt und Vorschau eingebaut
    labels: Definition was bei den Label Tags auf der Oberflaeche erscheinen soll. Wenn dies nicht definiert worde ist wird der Attributenname der Modellklasse genommen
    '''

    class Meta:
        # grouping: https://stackoverflow.com/questions/10366745/django-form-field-grouping#answer-10367761

        model = Book
        exclude = ['Id', 'user']
        LANGUAGES = (
            ('DE', _("Deutsch")),
            ('EN', _("Englisch")),
            ('FR', _("Französisch")),
            ('SP', _("Spanisch")),
        )
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
        fields = ('username', 'first_name', 'last_name', 'email', 'location', 'paypal', 'password1', 'password1')
        labels = {
            'location': _('Ort'),
        }

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.paypal = self.cleaned_data['paypal']

        if commit:
            user.save()
