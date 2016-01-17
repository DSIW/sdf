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
# manage.py dumpscript app.faq
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

    # Processing model: FAQ

    from app.models import FAQ
    from app_user.models import User

    admin = User.objects.filter(username='admin').first()



    faq = FAQ()
    faq.author = admin
    faq.position = 0
    faq.title = 'Wofür ist book²'
    faq.text = '<p><h3>Die Idee</h3></p><p>Auf book² kannst du deine gebrauchten Bücher zum Verkauf anbieten und dir direkt aus einer großen Auswahl von secondhand Büchern das nächste Schmuckstück aussuchen.</br> book² ist also eine Handelsplattform für secondhand Bücher aber gleichzeitig auch viel mehr als das! Du kannst ein Archiv erstellen, in dem du alle Bücher siehts, die du zur Zeit besitzt, und dir so stehts ein Überblick über dein Inventar verschaffen. <br /> <b>Nie mehr ein Buch doppelt kaufen, weil es irgendwo ganz hintem im Bücherregal vergessen wurde</b><br /><b> Nie mehr ein Buch stundenlang suchen, weil man es eigentlich gehabt habe aber es in Wirklichkeit schon längst wieder verkauft wurde.</b> <br /> </p><p><h3>Für wen ist book² gedacht?</h3><p><b>Für Dich, für Dich und ja, auch für Dich.</b></br> Jeder ist willkommen und kann hier seine Bücher zum Verkauf anbieten, sich Bücher kaufen und die vielen Funktionen von book² nutzen.</p><p><h3>Welche Bücher darf ich bei book² anbieten?</h3></p><p><b>Alle. Naja... fast.</b></br>Bei book² dürfen alle Bücher angeboten werden, die es in einem gut sortiertem Bücherladen, Secondhand-Geschäft oder Antiquar auch gibt. Nur bitten wir darum davon abzusehen Bücher anzubieten, die beispielsweise eine strafrechtliche Ermittlung nach sich ziehen könnten. book² hält sich das recht offen unerwünschte Bücher zu löschen.'
    faq.createdAt = dateutil.parser.parse("2015-11-08T14:22:59.793180+00:00")
    faq.updatedAt = dateutil.parser.parse("2015-11-08T14:22:59.793180+00:00")
    faq = importer.save_or_locate(faq)

    faq = FAQ()
    faq.author = admin
    faq.position = 1
    faq.title = 'Was ist das Archiv und wer kann es sich anschauen?'
    faq.text = '<p><b>Der Überblick über deine Bücher. Für Dich.</b> <br />Hier siehst du deine Bücher und kannst sie von hieraus zum Verkauf anbieten.<br /> Diesen Bereich kannst nur du sehen. Wenn du ein Buch verkaufen möchtest können es andere Nutzer in deinem Schaufenster finden.</p> <p>'
    faq.createdAt = dateutil.parser.parse("2015-11-08T14:22:59.793180+00:00")
    faq.updatedAt = dateutil.parser.parse("2015-11-08T14:22:59.793180+00:00")
    faq = importer.save_or_locate(faq)
