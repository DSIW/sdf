#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been automatically generated.
# Instead of changing it, create a file called import_helper.py
# and put there a class called ImportHelper(object) in it.
#
# This class will be specially casted so that instead of extending object,
# it will actually extend the class BasicImportHelper()
#
# That means you just have to overload the methods you want to
# change, leaving the other ones inteact.
#
# Something that you might want to do is use transactions, for example.
#
# Also, don't forget to add the necessary Django imports.
#
# This file was generated with the following command:
# ./manage.py dumpscript app.book
#
# to restore it, run
# manage.py runscript module_name.this_script_name
#
# example: if manage.py is at ./manage.py
# and the script is at ./some_folder/some_script.py
# you must make sure ./some_folder/__init__.py exists
# and run  ./manage.py runscript some_folder.some_script
import os, sys
from django.db import transaction

class BasicImportHelper(object):

    def pre_import(self):
        pass

    # You probably want to uncomment on of these two lines
    # @transaction.atomic  # Django 1.6
    # @transaction.commit_on_success  # Django <1.6
    def run_import(self, import_data):
        import_data()

    def post_import(self):
        pass

    def locate_similar(self, current_object, search_data):
        # You will probably want to call this method from save_or_locate()
        # Example:
        #   new_obj = self.locate_similar(the_obj, {"national_id": the_obj.national_id } )

        the_obj = current_object.__class__.objects.get(**search_data)
        return the_obj

    def locate_object(self, original_class, original_pk_name, the_class, pk_name, pk_value, obj_content):
        # You may change this function to do specific lookup for specific objects
        #
        # original_class class of the django orm's object that needs to be located
        # original_pk_name the primary key of original_class
        # the_class      parent class of original_class which contains obj_content
        # pk_name        the primary key of original_class
        # pk_value       value of the primary_key
        # obj_content    content of the object which was not exported.
        #
        # You should use obj_content to locate the object on the target db
        #
        # An example where original_class and the_class are different is
        # when original_class is Farmer and the_class is Person. The table
        # may refer to a Farmer but you will actually need to locate Person
        # in order to instantiate that Farmer
        #
        # Example:
        #   if the_class == SurveyResultFormat or the_class == SurveyType or the_class == SurveyState:
        #       pk_name="name"
        #       pk_value=obj_content[pk_name]
        #   if the_class == StaffGroup:
        #       pk_value=8

        search_data = { pk_name: pk_value }
        the_obj = the_class.objects.get(**search_data)
        #print(the_obj)
        return the_obj


    def save_or_locate(self, the_obj):
        # Change this if you want to locate the object in the database
        try:
            the_obj.save()
        except:
            print("---------------")
            print("Error saving the following object:")
            print(the_obj.__class__)
            print(" ")
            print(the_obj.__dict__)
            print(" ")
            print(the_obj)
            print(" ")
            print("---------------")

            raise
        return the_obj


importer = None
try:
    import import_helper
    # We need this so ImportHelper can extend BasicImportHelper, although import_helper.py
    # has no knowlodge of this class
    importer = type("DynamicImportHelper", (import_helper.ImportHelper, BasicImportHelper ) , {} )()
except ImportError as e:
    # From Python 3.3 we can check e.name - string match is for backward compatibility.
    if 'import_helper' in str(e):
        importer = BasicImportHelper()
    else:
        raise

import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

try:
    import dateutil.parser
except ImportError:
    print("Please install python-dateutil")
    sys.exit(os.EX_USAGE)

def run():
    importer.pre_import()
    importer.run_import(import_data)
    importer.post_import()

def import_data():
    # Initial Imports

    # Processing model: Book

    from app_book.models import Book
    from app_book.models import User

    app_book_1 = Book()
    app_book_1.user = User.objects.filter(username='mustermann').first()
    app_book_1.name = 'Lightweight Django'
    app_book_1.author = 'Julia Elman, Mark Lavin'
    app_book_1.language = 'EN'
    app_book_1.releaseDate = dateutil.parser.parse("2014-11-11")
    app_book_1.pageNumber = 243
    app_book_1.isbn10 = '149194594X'
    app_book_1.isbn13 = '978-1491945940'
    app_book_1.description = "Julia Elman has been working her brand of web skills for nearly a decade. She started out as a designer for an internal marketing group at a travel agency in Los Angeles, and quickly honed her skills as a web designer using HTML/CSS. Julia joined the Caktus Consulting Group in 2011 and is thrilled to work with some of the most talented developers this side of the Mississippi. She is actively involved with Girl Develop It RDU as an instructor to help contribute in educating women pursuing a career in technology. Mark is a lead Python/Django developer at Caktus Consulting Group in Carrboro, NC. He also runs a small homebrewing website written in Django called brewedbyus.com. He came to Python web development after a few years pricing derivatives on Wall Street. Mark maintains a number of open source projects primarily related to Django development and frequently contributes back to projects used by Caktus. When he isn't programming, Mark enjoys spending time with his wife and daughter, brewing beer, and running."
    app_book_1 = importer.save_or_locate(app_book_1)

    app_book_2 = Book()
    app_book_2.user = User.objects.filter(username='mustermann').first()
    app_book_2.name = 'Hands-on Django: Going Beyond the Polls'
    app_book_2.author = 'Brandon Lorenz'
    app_book_2.language = 'EN'
    app_book_2.releaseDate = dateutil.parser.parse("2016-03-25")
    app_book_2.pageNumber = 0
    app_book_2.isbn10 = '144936781X'
    app_book_2.isbn13 = '978-1449367817'
    app_book_2.description = ''
    app_book_2 = importer.save_or_locate(app_book_2)

    app_book_3 = Book()
    app_book_3.user = User.objects.filter(username='mustermann').first()
    app_book_3.name = 'Test-Driven Development with Python'
    app_book_3.author = 'Harry J.W. Percival'
    app_book_3.language = 'EN'
    app_book_3.releaseDate = dateutil.parser.parse("2014-06-19")
    app_book_3.pageNumber = 478
    app_book_3.isbn10 = '1449364829'
    app_book_3.isbn13 = '978-1449364823'
    app_book_3.description = ''
    app_book_3 = importer.save_or_locate(app_book_3)
