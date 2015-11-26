# -*- coding: utf-8 -*-

from django.test import TestCase
from app_book.forms import BookForm, OfferForm


class BookFormTests(TestCase):
    def setUp(self):
        self.form_data = {
            'name': 'BookName',
            'author': 'authorName',
            'language': 'Language',
            'releaseDate': '19.11.2016',
            'pageNumber': '13',
            'isbn10': '1-78528-753-2',
            'isbn13': '978-1-78528-753-4',
            'description': 'description',
        }

    def test_correctData(self):
        form = BookForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_missingAttribute(self):
        data = self.form_data.copy()

        for attrib in data.keys():
            if attrib in BookForm.base_fields.keys() and not BookForm.base_fields[attrib].required:
                continue
            # restore state
            data = self.form_data.copy()

            data[attrib] = ''
            form = BookForm(data=data)
            self.assertFalse(form.is_valid(), msg="Error at attribute: %s, empty string" % attrib)

            # TODO fix later: Forms should not accept whitespace only data
            #data[attrib] = ' '
            #form = BookForm(data=data)
            #self.assertFalse(form.is_valid(), msg="Error at attribute: %s, space string" % attrib)


    def test_intAttribute_isNotAnInt(self):
        data = self.form_data.copy()
        data['pageNumber'] = "NotAnInt"

        form = BookForm(data=data)
        self.assertFalse(form.is_valid())

    def test_intAttribute_isAnInt(self):
        data = self.form_data.copy()
        data['pageNumber'] = "1"

        form = BookForm(data=data)
        self.assertTrue(form.is_valid())
