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
# ./manage.py dumpscript app.user
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

from sdf import settings

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
    # Processing model: User

    from app_user.models import User

    auth_user_admin = User()
    auth_user_admin.password = 'pbkdf2_sha256$20000$f49atNcSl4xt$jBFjdFzW7X6ownYonQ7LK6EzMwshtYtLUxtdMqWGwks='
    auth_user_admin.last_login = dateutil.parser.parse("2015-11-08T14:22:59.793180+00:00")
    auth_user_admin.is_superuser = True
    auth_user_admin.username = 'admin'
    auth_user_admin.first_name = 'Admin'
    auth_user_admin.last_name = 'Admin'
    auth_user_admin.email = 'admin@admin.de'
    auth_user_admin.emailConfirm = True
    auth_user_admin.paypal = auth_user_admin.email
    auth_user_admin.location = 'Berlin'
    auth_user_admin.is_staff = True
    auth_user_admin.is_active = True
    auth_user_admin.date_joined = dateutil.parser.parse("2015-11-08T14:22:49.437731+00:00")
    auth_user_admin = importer.save_or_locate(auth_user_admin)

    auth_user_1 = User()
    auth_user_1.password = 'pbkdf2_sha256$20000$f49atNcSl4xt$jBFjdFzW7X6ownYonQ7LK6EzMwshtYtLUxtdMqWGwks='
    auth_user_1.last_login = dateutil.parser.parse("2015-11-08T14:22:59.793180+00:00")
    auth_user_1.is_superuser = False
    auth_user_1.username = 'max'
    auth_user_1.first_name = 'Max'
    auth_user_1.last_name = 'Mustermann'
    auth_user_1.email = 'max@book2.de'
    auth_user_1.emailConfirm = True
    auth_user_1.paypal = settings.SEED_MAX_PAYPAL or 'max@book2.de'
    auth_user_1.location = 'Berlin'
    auth_user_1.is_staff = False
    auth_user_1.is_active = True
    auth_user_1.date_joined = dateutil.parser.parse("2015-11-08T14:22:49.437731+00:00")
    auth_user_1 = importer.save_or_locate(auth_user_1)
    
    auth_user_1 = User()
    auth_user_1.password = 'pbkdf2_sha256$20000$f49atNcSl4xt$jBFjdFzW7X6ownYonQ7LK6EzMwshtYtLUxtdMqWGwks='
    auth_user_1.last_login = dateutil.parser.parse("2015-11-08T14:22:59.793180+00:00")
    auth_user_1.is_superuser = False
    auth_user_1.username = 'klaus_pseudo'
    auth_user_1.first_name = 'Klaus'
    auth_user_1.last_name = 'Strohmenger'
    auth_user_1.email = 's0535844@htw-berlin.de'
    auth_user_1.emailConfirm = True
    auth_user_1.paypal = 'klaus@book2.de'
    auth_user_1.location = 'Berlin'
    auth_user_1.is_staff = False
    auth_user_1.is_active = True
    auth_user_1.date_joined = dateutil.parser.parse("2015-12-12T15:20:45.437731+00:00")
    auth_user_1 = importer.save_or_locate(auth_user_1)

    auth_user_2 = User()
    auth_user_2.password = 'pbkdf2_sha256$20000$f49atNcSl4xt$jBFjdFzW7X6ownYonQ7LK6EzMwshtYtLUxtdMqWGwks='
    auth_user_2.last_login = dateutil.parser.parse("2015-11-08T14:22:59.793180+00:00")
    auth_user_2.is_superuser = False
    auth_user_2.username = 'martin'
    auth_user_2.first_name = 'Martin'
    auth_user_2.last_name = 'Mustermann'
    auth_user_2.email = 'martin@mustermann.de'
    auth_user_2.emailConfirm = True
    auth_user_2.paypal = settings.SEED_MARTIN_PAYPAL or 'martin@mustermann.de'
    auth_user_2.location = 'Hamburg'
    auth_user_2.is_staff = False
    auth_user_2.is_active = True
    auth_user_2.date_joined = dateutil.parser.parse("2015-11-08T14:22:49.437731+00:00")
    auth_user_2 = importer.save_or_locate(auth_user_2)

    auth_user_3 = User()
    auth_user_3.password = 'pbkdf2_sha256$20000$f49atNcSl4xt$jBFjdFzW7X6ownYonQ7LK6EzMwshtYtLUxtdMqWGwks='
    auth_user_3.last_login = dateutil.parser.parse("2015-11-08T14:22:59.793180+00:00")
    auth_user_3.is_superuser = False
    auth_user_3.username = 'marie'
    auth_user_3.first_name = 'Marie'
    auth_user_3.last_name = 'M'
    auth_user_3.email = 'marie@book2.de'
    auth_user_3.emailConfirm = True
    auth_user_3.paypal = 'marie@book2.de'
    auth_user_3.location = 'Berlin'
    auth_user_3.is_staff = False
    auth_user_3.is_active = True
    auth_user_3.date_joined = dateutil.parser.parse("2015-11-08T14:22:49.437731+00:00")
    auth_user_3 = importer.save_or_locate(auth_user_3)

    auth_user_4 = User()
    auth_user_4.password = 'pbkdf2_sha256$20000$6fimTWmnvrhn$ubTKr8VttnnIR3vp+2bsVJQb3Vxkz9MXkJfKvJf9Jic='
    auth_user_4.last_login = dateutil.parser.parse("2015-11-08T14:22:59.793180+00:00")
    auth_user_4.is_superuser = False
    auth_user_4.first_name = 'Andrej'
    auth_user_4.last_name = 'Beliakov'
    auth_user_4.email = 'andrej@andrej.in'
    auth_user_4.emailConfirm = True
    auth_user_4.paypal = 'andrej@andrej.in'
    auth_user_4.location = 'Berlin'
    auth_user_4.is_staff = False
    auth_user_4.is_active = True
    auth_user_4.date_joined = dateutil.parser.parse("2015-12-08T14:21:49.434251+00:00")
    auth_user_4 = importer.save_or_locate(auth_user_4)

    auth_user_5 = User()
    auth_user_5.password = 'pbkdf2_sha256$20000$f49atNcSl4xt$jBFjdFzW7X6ownYonQ7LK6EzMwshtYtLUxtdMqWGwks='
    auth_user_5.last_login = dateutil.parser.parse("2015-11-08T14:22:59.793180+00:00")
    auth_user_5.is_superuser = False
    auth_user_5.first_name = 'Jens'
    auth_user_5.last_name = 'Ottmann'
    auth_user_5.email = 'jens@book2.de'
    auth_user_5.emailConfirm = True
    auth_user_5.paypal = 'jens@book2.de'
    auth_user_5.location = 'Berlin'
    auth_user_5.is_staff = False
    auth_user_5.is_active = True
    auth_user_5.date_joined = dateutil.parser.parse("2015-12-08T14:21:49.434251+00:00")
    auth_user_5 = importer.save_or_locate(auth_user_5)

