# coding=utf-8
from django.test import TestCase
from app_book.forms import BookForm

'''
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
        form_data_copy = self.form_data
        # force new empty line for next print
        print()

        for attrib in form_data_copy.keys():
            # restore state
            form_data_copy = self.form_data

            print(attrib)
            form_data_copy[attrib] = ''
            form = BookForm(data=form_data_copy)
            self.assertFalse(form.is_valid(), msg="Error at attribute: %s, empty string" % attrib)

        for attrib in form_data_copy.keys():
            # restore state
            form_data_copy = self.form_data

            print(attrib)
            form_data_copy[attrib] = ' '
            form = BookForm(data=form_data_copy)
            self.assertFalse(form.is_valid(), msg="Error at attribute: %s, space string" % attrib)

    def test_intAttribute_isNotAnInt(self):
        self.form_data['pageNumber'] = "NotAnInt"
        form = BookForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_intAttribute_isAnInt(self):
        self.form_data['pageNumber'] = "1"
        form = BookForm(data=self.form_data)
        self.assertTrue(form.is_valid())

'''