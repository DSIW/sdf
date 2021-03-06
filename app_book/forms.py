# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.datastructures import SortedDict

from .models import Book, Offer, Counteroffer

from app.widgets import CustomFileInput
from app.templatetags.template_extras import currency


class BookForm(forms.ModelForm):
    '''
    Klasse zum erstellen der Buch Form
    widgets: Defintion wie die Eingabefelder auszusehen haben. Hier am Beispiel css Klasse von Bootstrap genutzt und Vorschau eingebaut
    labels: Definition was bei den Label Tags auf der Oberflaeche erscheinen soll. Wenn dies nicht definiert worde ist wird der Attributenname der Modellklasse genommen
    '''
    delete_saved_image = forms.BooleanField(required=False, label='Bild löschen')

    ordered_field_names = ('name', 'author', 'language', 'releaseDate', 'pageNumber', 'isbn10', 'isbn13', 'image', 'delete_saved_image', 'description')

    def __init__(self, *args, **kwargs):
        self.book = kwargs.get('instance')
        super(BookForm, self).__init__(*args, **kwargs)
        self.rearrange_field_order()
        self.fields['language'].initial = 'de'
        if not (self.book and self.book.image):
            del self.fields['delete_saved_image']

    class Meta:
        model = Book
        exclude = ['Id', 'user']
        widgets = {
            'language': forms.Select(choices=map(lambda a: (a[0], ugettext(a[1])+' ('+a[0].upper()+')'), settings.LANGUAGES)),
            'releaseDate': forms.DateInput(attrs={'class': 'datepicker'}),
            'image': CustomFileInput(),
        }
        labels = {
            'name': _('Buchname'),
            'author': _('Author'),
            'language': _('Sprache'),
            'releaseDate': _('Veröffentlichungsdatum'),
            'pageNumber': _('Seitenanzahl'),
            'isbn10': _('ISBN-10'),
            'isbn13': _('ISBN-13'),
            'image': _('Bild'),
            'description': _('Beschreibung'),
        }

    def rearrange_field_order(self):
        original_fields = self.fields
        new_fields = SortedDict()

        for field_name in self.ordered_field_names:
            field = original_fields.get(field_name)
            if field:
                new_fields[field_name] = field

        self.fields = new_fields

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['active', 'price', 'shipping_price', 'allow_counteroffers']
        labels = {
            'active': _('Verkaufen'),
            'price': _('Buchpreis'),
            'shipping_price': _('Versandpreis'),
            'allow_counteroffers': _('Akzeptiere Preisvorschläge'),
        }

class PublishOfferForm(OfferForm):
    class Meta(OfferForm.Meta):
        exclude = ['active']

class CounterofferForm(forms.ModelForm):
    class Meta:
        model = Counteroffer
        fields = ['price']
        labels = {
            'price': _('Preisvorschlag'),
        }

    def clean(self):
        cleaned_data = super(CounterofferForm, self).clean()
        price_myself = cleaned_data.get("price")
        offer_price = self.instance.offer.totalPrice()
        if price_myself > offer_price:
            msg = 'Der von Ihnen vorgeschlagene Preis ist höher als der Sofortkauf-Preis von ' + currency(offer_price)
            self.add_error('price', msg)


