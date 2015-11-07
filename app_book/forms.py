# coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.utils import ErrorDict

from .models import Book, Offer

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
