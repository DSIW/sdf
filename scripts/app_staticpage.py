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
# ./manage.py dumpscript app.staticpage
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

from django.conf import settings

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
    # Processing model: StaticPage

    from app.models import StaticPage

    static_page_imprint = StaticPage()
    static_page_imprint.name = 'imprint'
    static_page_imprint.title = 'Impressum'
    static_page_imprint.content = '<b>Firma:</b> Book² GmbH\n<b>Geschäftsführer:</b> Herr Max Mustermann\n<b>SteuerID:</b> 00000000000000000000\n<b>Straße:</b> Musterstr. 1\n<b>Ort:</b> 12345 Musterstadt\n<b>Registereintrag:</b>\nRegisternummer: HRA 00000\nRegistergericht: Amtsgericht Musterstadt\nUST-IdNr.: DE000000000\n\n<b>Kontakt:</b>\nTelefon: (0000) 000 000 (0000 Ct./Anruf dt. Festnetz, max. 2000 Ct./Anruf dt. Mobilfunk)\nServicezeiten: Montag bis Samstag von 8:00 bis 20:00 Uhr\nE-Mail: info@book2.de\n\n<b>Copyright:</b>\n\nJedes Website-Design, jeder Text, jede Auswahl bzw. jedes Layout davon und jede Software sind rechtlich geschütztes Eigentum von Book² GmbH (Copyright © 2015 Book² GmbH, ALLE RECHTE VORBEHALTEN). Das Kopieren oder die Reproduktion (inklusive des Ausdrucks auf Papier) der gesamten Website bzw. von Teilen dieser Website werden nur zu dem Zweck gestattet, diese Website als Einkaufsressource zu verwenden.\nJede andere Verwendung der auf dieser Website verfügbaren Materialien bzw. Informationen -- inklusive der Reproduktion, des Weitervertriebs, der Veränderung und der Veröffentlichung zu einem anderen als dem oben genannten Zweck -- ist untersagt.'
    static_page_imprint = importer.save_or_locate(static_page_imprint)

    static_page_privacy = StaticPage()
    static_page_privacy.name = 'privacy'
    static_page_privacy.title = 'Datenschutz'
    static_page_privacy.content = 'Mit Beginn der Registrierung als Nutzer/in werden die von Ihnen eingegebenen oder mit Ihrer Nutzung automatisch anfallenden Daten - auch Ihre IP-Adresse - verarbeitet. Soweit diese auf Ihre Person und nicht nur auf eine fingierte Identität verweisen, handelt es sich um personenbezogene Daten. Darum gelten auch für das Book² die einschlägigen Datenschutzgesetze. Diese verlangen vor allem die eingehende Information über Art und Umfang der Erhebung von personenbezogenen Daten und Art und Weise ihrer weiteren Verarbeitung.\n\nNach dem Login können Sie diese Daten jederzeit über Ihr persönliches Profil einsehen, wenn Sie auf Ihren Namen klicken. Sie können Ihre Profildaten um weitere freiwillige Angaben ergänzen.\nWir senden Ihnen in unregelmäßigen Abständen Nachrichten per E-Mail zu, um Sie über Neuigkeiten zu informieren.\n\n<b>Einwilligung:</b>\n\nMit der Registrierung und Nutzung von Book² geben Sie, in Kenntnis dieser Erläuterungen, Ihre Einwilligung zu der bezeichneten Datenerhebung und -verwendung. Diese Einwilligung ist jederzeit widerrufbar durch eine entsprechende Erklärung gegenüber der Book²-Administration. Schreiben Sie dazu eine E-Mail an: support@book2.de.'
    static_page_privacy = importer.save_or_locate(static_page_privacy)

    static_page_team = StaticPage()
    static_page_team.name = 'agb'
    static_page_team.title = 'AGB'
    static_page_team.content = '<b>Allgemeine Geschäftsbedingungen von Book²:</b>\n\nBook² ist ein Shop der Book² GmbH. Book² bietet einen Marktplatz für natürliche Personen zum Kaufen und Verkaufen von gebrauchten Bücher an. Für das Anbieten, Verkaufen und Kaufen von Büchern ist ein Nutzerkonto erforderlich. Es ist verboten, Artikel, deren Angebot, Verkauf oder Erwerb gegen gesetzliche Vorschriften oder Rechte Dritter verstoßen bzw. sittenwidrig sind, auf Book² anzubieten oder zu bewerben. Book² behält sich vor, Schaufenster mit sittenwidrigen Inhalten zu sperren.\n\nFür den Vertragsschluss steht nur die deutsche Sprache zur Verfügung. Verträge kommen ausschließlich zwischen den Nutzern (Käufern und Verkäufern) dieses Marktplatztes zustande. Book² selbst wird nicht Vertragspartner. Die Präsentation der Waren stellt kein bindendes Angebot dar. Erst durch das Anklicken des Buttons "Jetzt kaufen" bzw. Abschicken eines Preisvorschlags geben Sie ein bindendes Angebot ab. Ein Vertrag kommt zwischen Käufer und Verkäufer zustande, wenn der Verkäufer die Ware zustellt.<br><br>Für Downloads digitaler Inhalte gilt Folgendes: Die Inhalte sind urheberrechtlich geschützt; Sie verpflichten sich, die Urheberrechte anzuerkennen und einzuhalten. Eine darüber hinaus gehende Nutzung ist nur im Rahmen und unter Beachtung der Schrankenbestimmungen des Urheberrechtes (§§ 44 a ff. UrhG) zulässig.\n\nAlle Preise sind in Euro (EUR) inklusive der gesetzlichen Mehrwertsteuer (zuzüglich etwaiger Versandkosten). Sie können die Ware ausschließlich per Paypal bezahlen. Zur Nutzung von Paypal ist ein Benutzerkonto erforderlich.\n\nEine Haftung von Book² ist ausgeschlossen.'
    static_page_team = importer.save_or_locate(static_page_team)

