# -*- coding: utf-8 -*-
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import TestCase
from app_book.forms import BookForm, OfferForm


class BookFormTests(TestCase):
    def setUp(self):
        with open('fixtures/image1.jpg', 'rb') as img:
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
        with open('fixtures/image1.jpg', 'rb') as img:
            image = SimpleUploadedFile(img.name, img.read(), content_type='image/jpeg')
        form = BookForm(self.form_data, {'image': image})
        for error in form.errors:
            print("Errors:")
            print(error)
        self.assertTrue(form.is_valid())

    def test_missingAttribute(self):
        data = self.form_data.copy()

        for attrib in data.keys():
            if attrib in BookForm.base_fields.keys() and not BookForm.base_fields[attrib].required:
                continue
            # restore state
            data = self.form_data.copy()

            data[attrib] = ''
            form = BookForm(data)
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
        with open('fixtures/image1.jpg', 'rb') as img:
            image = SimpleUploadedFile(img.name, img.read(), content_type='image/jpeg')

        form = BookForm(data, {'image': image})
        self.assertTrue(form.is_valid())
