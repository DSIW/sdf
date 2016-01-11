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
    from app_book.models import Offer

    app_book = Book()
    app_book.user = User.objects.filter(username='max').first()
    app_book.name = 'Lightweight Django'
    app_book.author = 'Julia Elman, Mark Lavin'
    app_book.language = 'EN'
    app_book.releaseDate = dateutil.parser.parse("2014-11-11")
    app_book.pageNumber = 243
    app_book.image = 'images/books/book_2.jpg'
    app_book.isbn10 = '149194594X'
    app_book.isbn13 = '978-1491945940'
    app_book.description = "Julia Elman has been working her brand of web skills for nearly a decade. She started out as a designer for an internal marketing group at a travel agency in Los Angeles, and quickly honed her skills as a web designer using HTML/CSS. Julia joined the Caktus Consulting Group in 2011 and is thrilled to work with some of the most talented developers this side of the Mississippi. She is actively involved with Girl Develop It RDU as an instructor to help contribute in educating women pursuing a career in technology. Mark is a lead Python/Django developer at Caktus Consulting Group in Carrboro, NC. He also runs a small homebrewing website written in Django called brewedbyus.com. He came to Python web development after a few years pricing derivatives on Wall Street. Mark maintains a number of open source projects primarily related to Django development and frequently contributes back to projects used by Caktus. When he isn't programming, Mark enjoys spending time with his wife and daughter, brewing beer, and running."
    app_book = importer.save_or_locate(app_book)

    offer = Offer()
    offer.updated = dateutil.parser.parse("2015-12-18T11:00:00.000000+00:00")
    offer.seller_user = User.objects.filter(username='max').first()
    offer.book = Book.objects.filter(name = 'Lightweight Django').first()
    offer.price = 7.0
    offer.shipping_price = 1.0
    offer.active = True
    offer = importer.save_or_locate(offer)

    app_book = Book()
    app_book.user = User.objects.filter(username='max').first()
    app_book.name = 'Hands-on Django: Going Beyond the Polls'
    app_book.author = 'Brandon Lorenz'
    app_book.language = 'EN'
    app_book.releaseDate = dateutil.parser.parse("2016-03-25")
    app_book.pageNumber = 300
    app_book.image = 'images/books/book_3.jpg'
    app_book.isbn10 = '144936781X'
    app_book.isbn13 = '978-1449367817'
    app_book.description = ''
    app_book = importer.save_or_locate(app_book)

    offer = Offer()
    offer.updated = dateutil.parser.parse("2015-12-18T11:00:00.000000+00:00")
    offer.seller_user = User.objects.filter(username='max').first()
    offer.book = Book.objects.filter(name = 'Hands-on Django: Going Beyond the Polls').first()
    offer.price = 7.0
    offer.shipping_price = 1.0
    offer.active = True
    offer = importer.save_or_locate(offer)

    app_book = Book()
    app_book.user = User.objects.filter(username='martin').first()
    app_book.name = 'Test-Driven Development with Python'
    app_book.author = 'Harry J.W. Percival'
    app_book.language = 'EN'
    app_book.releaseDate = dateutil.parser.parse("2014-06-19")
    app_book.pageNumber = 478
    app_book.image = 'images/books/book_15.jpg'
    app_book.isbn10 = '1449364829'
    app_book.isbn13 = '978-1449364823'
    app_book.description = ''
    app_book = importer.save_or_locate(app_book)

    app_book = Book()
    app_book.user = User.objects.filter(username='martin').first()
    app_book.name = 'Die Betrogene'
    app_book.author = 'Charlotte Link'
    app_book.language = 'DE'
    app_book.releaseDate = dateutil.parser.parse("2015-09-02")
    app_book.pageNumber = 640
    app_book.image = 'images/books/book_4.jpg'
    app_book.isbn10 = '3734100852'
    app_book.isbn13 = '978-3734100857'
    app_book.description = '''
Einsam wacht, wer um die Schuld weiß ...

Um ein glückliches Leben betrogen – so fühlt sich Kate Linville, Polizistin bei Scotland Yard. Kontaktscheu und einsam, gibt es nur einen Menschen, den sie liebt: ihren Vater. Als dieser in seinem Haus grausam ermordet wird, verliert Kate ihren letzten Halt. Da sie dem alkoholkranken Ermittler vor Ort nicht traut, macht sie sich selbst auf die Spur dieses mysteriösen Verbrechens. Und entlarvt die Vergangenheit ihres Vaters als Trugbild, denn er war nicht der, für den sie ihn hielt.
'''
    app_book = importer.save_or_locate(app_book)

    app_book = Book()
    app_book.user = User.objects.filter(username='martin').first()
    app_book.name = 'Honigtot'
    app_book.author = 'Hanni Münzer'
    app_book.language = 'DE'
    app_book.releaseDate = dateutil.parser.parse("2015-04-13")
    app_book.pageNumber = 480
    app_book.image = 'images/books/book_5.jpg'
    app_book.isbn10 = '3492307256'
    app_book.isbn13 = '978-3492307256'
    app_book.description = '''
GEWIDMET DEN MUTIGEN FRAUEN DES WIDERSTANDS IM ZWEITEN WELTKRIEG. SIE SIND HELDINNEN.
*********************************************************************************************************************************************
»Mein größter Fehler war es, dass ich Hitler das Gewehr weggenommen habe. Hätte ich ihn sich nur umbringen lassen!« Helene Hanfstängl, 1959
*********************************************************************************************************************************************
Wie weit geht eine Mutter, um ihre Kinder zu retten? Wie weit geht eine Tochter, um ihren Vater zu rächen? Wie kann eine tiefe, alles verzehrende Liebe die Generationen überdauern und alte Wunden heilen?
Als sich die junge Felicity auf die Suche nach ihrer Mutter macht, stößt sie dabei auf ein quälendes Geheimnis ihrer Familiengeschichte. Ihre Nachforschungen führen sie zurück in das dunkelste Kapitel unserer Vergangenheit und zum dramatischen Schicksal ihrer Urgroßmutter Elisabeth und deren Tochter Deborah. Ein Netz aus Liebe, Schuld und Sühne umfing beide Frauen und warf über Generationen einen Schatten auf Felicitys eigenes Leben.
'''
    app_book = importer.save_or_locate(app_book)

    app_book = Book()
    app_book.user = User.objects.filter(username='martin').first()
    app_book.name = 'Star Wars(TM) Das Erwachen der Macht. Raumschiffe und Fahrzeuge'
    app_book.author = 'k.A.'
    app_book.language = 'DE'
    app_book.releaseDate = dateutil.parser.parse("2015-12-18")
    app_book.pageNumber = 48
    app_book.image = 'images/books/book_6.jpg'
    app_book.isbn10 = '3831028788'
    app_book.isbn13 = '978-3831028788'
    app_book.description = '''
Atemberaubende Einblicke in die Technik von „STAR WARS™: Das Erwachen der Macht“ mit einzigartigen Darstellungen von den Fahrzeugen. Großformatige Illustrationen zeigen und erklären ihre neuen Waffen sowie faszinierende technische Details.
'''
    app_book = importer.save_or_locate(app_book)

    offer = Offer()
    offer.updated = dateutil.parser.parse("2015-12-18T11:00:00.000000+00:00")
    offer.seller_user = User.objects.filter(username='martin').first()
    offer.book = Book.objects.filter(name = 'Star Wars(TM) Das Erwachen der Macht. Raumschiffe und Fahrzeuge').first()
    offer.price = 55.0
    offer.shipping_price = 5.0
    offer.active = True
    offer = importer.save_or_locate(offer)

    app_book = Book()
    app_book.user = User.objects.filter(username='martin').first()
    app_book.name = 'Was ich noch sagen wollte'
    app_book.author = 'Helmut Schmidt'
    app_book.language = 'DE'
    app_book.releaseDate = dateutil.parser.parse("2015-12-11")
    app_book.pageNumber = 239
    app_book.image = 'images/books/book_7.jpg'
    app_book.isbn10 = '340667612X'
    app_book.isbn13 = '978-3406676123'
    app_book.description = '''
Sieben Jahre nach Außer Dienst legte Helmut Schmidt ein neues eigenes Buch vor. Seine Ausgangsfrage lautet: Brauchen wir heute noch Vorbilder, und wenn ja, zu welchen Zielen sollen sie uns anleiten? Schmidt erzählt von Menschen, die ihn prägten und an deren Beispiel er sich orientierte.

Politik ist pragmatisches Handeln zu sittlichen Zwecken, hat Helmut Schmidt einmal gesagt. Weil er stets pragmatisch handelte, hat man ihm früh das Etikett des "Machers" angeheftet. Dass seiner Politik aber immer ein strenges sittliches Koordinatensystem zugrunde lag, ahnten die wenigsten. Und die Bezugsgrößen in Schmidts ethischer Grundorientierung sind unverrückbar geblieben. Die frühe Lektüre von Mark Aurel und Cicero, die Beschäftigung mit Kant und Weber, die Vertiefung in die Philosophie Karl Poppers sind entscheidende Wegmarken in der Entwicklung eines Politikers, der den Wählern nie nach dem Mund redete. Ob Schmidt berichtet, wie sich ihm in Gesprächen mit dem ägyptischen Präsidenten Sadat die gemeinsamen Wurzeln von Judentum, Christentum und Islam erschlossen oder wie in den Begegnungen mit Deng Xiaoping das System des Konfuzianismus bestätigt wurde: Im Mittelpunkt steht stets die persönliche Faszination. Im einleitenden Kapitel "Frühe Prägungen" schreibt Schmidt über seine Schulzeit, über acht Jahre als Soldat – und über seine Frau Loki.
'''
    app_book = importer.save_or_locate(app_book)

    offer = Offer()
    offer.updated = dateutil.parser.parse("2015-12-02T12:00:00.000000+00:00")
    offer.seller_user = User.objects.filter(username='martin').first()
    offer.book = Book.objects.filter(name = 'Was ich noch sagen wollte').first()
    offer.price = 14.0
    offer.shipping_price = 3.0
    offer.active = True
    offer = importer.save_or_locate(offer)

    app_book = Book()
    app_book.user = User.objects.filter(username='martin').first()
    app_book.name = 'Passagier 23: Psychothriller'
    app_book.author = 'Sebastian Fitzek'
    app_book.language = 'DE'
    app_book.releaseDate = dateutil.parser.parse("2015-12-18")
    app_book.pageNumber = 432
    app_book.image = 'images/books/book_8.jpg'
    app_book.isbn10 = '3426510170'
    app_book.isbn13 = '978-3426510179'
    app_book.description = '''
Jedes Jahr verschwinden auf hoher See rund 20 Menschen spurlos von Kreuzfahrtschiffen. Noch nie kam jemand zurück. Bis jetzt ... 

Martin Schwartz, Polizeipsychologe, hat vor fünf Jahren Frau und Sohn verloren. Es geschah während eines Urlaubs auf dem Kreuzfahrtschiff „Sultan of the Seas“ – niemand konnte ihm sagen, was genau geschah. Martin ist seither ein psychisches Wrack und betäubt sich mit Himmelfahrtskommandos als verdeckter Ermittler. 
Mitten in einem Einsatz bekommt er den Anruf einer seltsamen alten Dame, die sich als Thrillerautorin bezeichnet: Er müsse unbedingt an Bord der „Sultan“ kommen, es gebe Beweise dafür, was seiner Familie zugestoßen ist. Nie wieder wollte Martin den Fuß auf ein Schiff setzen – und doch folgt er dem Hinweis und erfährt, dass ein vor Wochen auf der „Sultan“ verschwundenes Mädchen wieder aufgetaucht ist. Mit dem Teddy seines Sohnes im Arm … 
'''
    app_book = importer.save_or_locate(app_book)

    app_book = Book()
    app_book.user = User.objects.filter(username='martin').first()
    app_book.name = 'Darm mit Charme: Alles über ein unterschätztes Organ'
    app_book.author = 'Giulia Enders'
    app_book.language = 'DE'
    app_book.releaseDate = dateutil.parser.parse("2014-03-03")
    app_book.pageNumber = 288
    app_book.image = 'images/books/book_9.jpg'
    app_book.isbn10 = '3550080417'
    app_book.isbn13 = '978-3550080418'
    app_book.description = '''
Ausgerechnet der Darm! Das schwarze Schaf unter den Organen, das einem doch bisher eher unangenehm war. Aber dieses Image wird sich ändern. Denn Übergewicht, Depressionen und Allergien hängen mit einer gestörten Balance der Darmflora zusammen. Das heißt umgekehrt: Wenn wir uns in unserem Körper wohl fühlen, länger leben und glücklicher werden wollen, müssen wir unseren Darm pflegen. Das zumindest legen die neuesten Forschungen nahe. In diesem Buch erklärt die junge Wissenschaftlerin Giulia Enders vergnüglich, welch ein hochkomplexes und wunderbares Organ der Darm ist. Er ist der Schlüssel zu einem gesunden Körper und einem gesunden Geist und eröffnet uns einen ganz neuen Blick durch die Hintertür.
'''
    app_book = importer.save_or_locate(app_book)

    app_book = Book()
    app_book.user = User.objects.filter(username='martin').first()
    app_book.name = 'Altes Land'
    app_book.author = 'Dörte Hansen'
    app_book.language = 'DE'
    app_book.releaseDate = dateutil.parser.parse("2015-02-16")
    app_book.pageNumber = 288
    app_book.image = 'images/books/book_10.jpg'
    app_book.isbn10 = '3813506479'
    app_book.isbn13 = '978-3813506471'
    app_book.description = '''
Zwei Frauen, ein altes Haus und eine Art von Familie

Das „Polackenkind“ ist die fünfjährige Vera auf dem Hof im Alten Land, wohin sie 1945 aus Ostpreußen mit ihrer Mutter geflohen ist. Ihr Leben lang fühlt sie sich fremd in dem großen, kalten Bauernhaus und kann trotzdem nicht davon lassen. Bis sechzig Jahre später plötzlich ihre Nichte Anne vor der Tür steht. Sie ist mit ihrem kleinen Sohn aus Hamburg-Ottensen geflüchtet, wo ehrgeizige Vollwert-Eltern ihre Kinder wie Preispokale durch die Straßen tragen – und wo Annes Mann eine Andere liebt. Vera und Anne sind einander fremd und haben doch viel mehr gemeinsam, als sie ahnen. 

Mit scharfem Blick und trockenem Witz erzählt Dörte Hansen von zwei Einzelgängerinnen, die überraschend finden, was sie nie gesucht haben: eine Familie.
'''
    app_book = importer.save_or_locate(app_book)

    offer = Offer()
    offer.updated = dateutil.parser.parse("2015-11-30T11:00:00.000000+00:00")
    offer.seller_user = User.objects.filter(username='martin').first()
    offer.book = Book.objects.filter(name = 'Altes Land').first()
    offer.price = 10.0
    offer.shipping_price = 1.0
    offer.active = True
    offer = importer.save_or_locate(offer)

    app_book = Book()
    app_book.user = User.objects.filter(username='martin').first()
    app_book.name = 'Jamies Superfood für jeden Tag'
    app_book.author = 'Jamie Oliver'
    app_book.language = 'DE'
    app_book.releaseDate = dateutil.parser.parse("2015-10-15")
    app_book.pageNumber = 312
    app_book.image = 'images/books/book_11.jpg'
    app_book.isbn10 = '3831028931'
    app_book.isbn13 = '978-3831028931'
    app_book.description = '''
Nach einer persönlichen Reise, bei der seine Ernährung im Vordergrund stand, präsentiert Jamie Oliver das Ergebnis dieser Erfahrung: ein Kochbuch für gesunden Genuss mit dem Versprechen, "(...) jedes Rezept darin ist eine gute Wahl". Das Prinzip ist eine einfache Gleichung: genial kochen + gesund genießen = glücklich sein. So hat Jamie über 90 originelle Rezepte für Frühstück, Mittag- und Abendessen entwickelt, die einem fundierten ernährungswissenschaftlichen Konzept folgen. Vom Protein-Porridge mit Haferflocken, Samen, Nüssen und Quinoa über Fisch-Tacos mit Kiwi-Limetten-Chili-Salsa bis hin zur Kürbislasagne mit Spinat, Hüttenkäse und Samen: Herausgekommen sind alltagstaugliche Gerichte, die kalorienarm, reich an Nährstoffen und voller Aroma sind Superfood eben, für ganz viel Genuss und wenig Reue.

"Dieses Buch soll Ihnen die Tür zu einem bewussteren Umgang mit Essen öffnen, zu Mahlzeiten, die nicht nur satt machen, Energie liefern und die Laune heben, sondern auch heilende Kräfte haben. Ich möchte Ihnen mehr Wissen über gesunde Ernährung vermitteln und Ihnen zeigen, wie man eine ausgewogene Mahlzeit zusammenstellt." Jamie Oliver
'''
    app_book = importer.save_or_locate(app_book)

    offer = Offer()
    offer.updated = dateutil.parser.parse("2015-12-10T10:00:00.000000+00:00")
    offer.seller_user = User.objects.filter(username='martin').first()
    offer.book = Book.objects.filter(name = 'Jamies Superfood für jeden Tag').first()
    offer.price = 21.0
    offer.shipping_price = 3.0
    offer.active = True
    offer = importer.save_or_locate(offer)

    app_book = Book()
    app_book.user = User.objects.filter(username='martin').first()
    app_book.name = 'Das Joshua-Profil'
    app_book.author = 'Sebastian Fitzek'
    app_book.language = 'DE'
    app_book.releaseDate = dateutil.parser.parse("2015-10-26")
    app_book.pageNumber = 432
    app_book.image = 'images/books/book_12.jpg'
    app_book.isbn10 = '3785725450'
    app_book.isbn13 = '978-3785725450'
    app_book.description = '''
Der erfolglose Schriftsteller Max ist ein gesetzestreuer Bürger. Anders als sein Bruder Cosmo, der in der Sicherheitsverwahrung einer psychiatrischen Anstalt sitzt, hat Max sich noch niemals im Leben etwas zuschulden kommen lassen. Doch in wenigen Tagen wird er eines der entsetzlichsten Verbrechen begehen, zu denen ein Mensch überhaupt fähig ist. Nur, dass er heute noch nichts davon weiß ... im Gegensatz zu denen, die ihn töten wollen, bevor es zu spät ist.
'''
    app_book = importer.save_or_locate(app_book)

    offer = Offer()
    offer.updated = dateutil.parser.parse("2015-12-10T10:00:00.000000+00:00")
    offer.seller_user = User.objects.filter(username='martin').first()
    offer.book = Book.objects.filter(name = 'Das Joshua-Profil').first()
    offer.price = 5.0
    offer.shipping_price = 1.0
    offer.active = True
    offer = importer.save_or_locate(offer)

    app_book = Book()
    app_book.user = User.objects.filter(username='marie').first()
    app_book.name = 'Dead Mountain: The Untold True Story of the Dyatlov Pass Incident'
    app_book.author = 'Donnie Eichar'
    app_book.language = 'EN'
    app_book.releaseDate = dateutil.parser.parse("2013-11-15")
    app_book.pageNumber = 288
    app_book.image = 'images/books/book_13.jpg'
    app_book.isbn10 = '1452112746'
    app_book.isbn13 = '978-1452112749'
    app_book.description = '''
In February 1959, a group of nine hikers in the Russian Ural Mountains died in a mysterious fashion on the eastern side of an elevation known as Dead Mountain. Eerie aspects of the incident - unsettling and unexplained causes of death, a strange final photograph by one of the hikers and signs of radioactivity - have led to decades of speculation over what really happened. This gripping work of literary nonfiction delves into the mystery through unprecedented access to the hikers' own journals and photographs (many translated and reproduced in the book); unseen government records; and dozens of interviews, including with the only surviving hiker; and the author's retracing the hikers' fateful journey.
'''
    app_book = importer.save_or_locate(app_book)

    offer = Offer()
    offer.updated = dateutil.parser.parse("2015-12-10T12:00:00.000000+00:00")
    offer.seller_user = User.objects.filter(username='marie').first()
    offer.book = Book.objects.filter(name = 'Dead Mountain: The Untold True Story of the Dyatlov Pass Incident').first()
    offer.price = 14.0
    offer.shipping_price = 3.0
    offer.active = True
    offer = importer.save_or_locate(offer)

    app_book = Book()
    app_book.user = User.objects.filter(username='marie').first()
    app_book.name = 'Der Mann ohne Eigenschaften'
    app_book.author = 'Robert Musil'
    app_book.language = 'DE'
    app_book.releaseDate = dateutil.parser.parse("2013-07-31")
    app_book.pageNumber = 992
    app_book.image = 'images/books/book_14.jpg'
    app_book.isbn10 = '3730600400'
    app_book.isbn13 = '978-3730600405'
    app_book.description = '''
Ulrich heißt der 'Mann ohne Eigenschaften', er ist Mathematiker, Philosoph und stellt sich permanent selbst in Frage. Ulrich steht für Robert Musils literarisches Vorhaben, die Wirklichkeit als das ziellose Ergebnis einer Überfülle von Möglichkeiten zu schildern. Der Held dieses Romans begegnet einem wahren Panoptikum aus Mit- und Gegenspielern: Akteuren der Wiener Diplomatie und des Großkapitals, Schwärmern, Revolutionären, einem Sexualmörder, einer esoterischen Salonkönigin. Der Leser blickt hier in das 'unbestechliche Bild eines Zerrspiegels' gebannt und fasziniert.
'''
    app_book = importer.save_or_locate(app_book)

    offer = Offer()
    offer.updated = dateutil.parser.parse("2015-12-19T12:00:00.000000+00:00")
    offer.seller_user = User.objects.filter(username='marie').first()
    offer.book = Book.objects.filter(name = 'Der Mann ohne Eigenschaften').first()
    offer.price = 30.0
    offer.shipping_price = 6.0
    offer.active = True
    offer = importer.save_or_locate(offer)

    app_book = Book()
    app_book.user = User.objects.filter(username='marie').first()
    app_book.name = 'Berge des Wahnsinns: Eine Horrorgeschichte'
    app_book.author = 'H. P. Lovecraft '
    app_book.language = 'DE'
    app_book.releaseDate = dateutil.parser.parse("1997-11-29")
    app_book.pageNumber = 192
    app_book.image = 'images/books/book_16.jpg'
    app_book.isbn10 = '3518392603'
    app_book.isbn13 = '978-3518392607'
    app_book.description = '''
»Der Held entdeckt zuerst die Ruinen einer Stadt, dann immer deutlichere Anzeichen für eine untergegangene Zivilisation... Die Stadt ist der bevorzugte Ort der Veränderung unter dem doppelten Vorzeichen des sehr Alten und des Ungeheuerlichen. Sie ist ein Palimpsest, das der Erzähler unter Gefährdung seiner geistigen Integrität zu entziffern verpflichtet ist...« Gilles Menegaldo
'''

    app_book = importer.save_or_locate(app_book)

    offer = Offer()
    offer.updated = dateutil.parser.parse("2015-12-18T12:00:00.000000+00:00")
    offer.seller_user = User.objects.filter(username='marie').first()
    offer.book = Book.objects.filter(name = 'Berge des Wahnsinns: Eine Horrorgeschichte').first()
    offer.price = 10.0
    offer.shipping_price = 2.5
    offer.active = True
    offer = importer.save_or_locate(offer)

    app_book = Book()
    app_book.user = User.objects.filter(email='andrej@andrej.in').first()
    app_book.name = 'Ночной Дозор'
    app_book.author = 'Сергей Лукьяненко'
    app_book.language = 'RU'
    app_book.releaseDate = dateutil.parser.parse("2004")
    app_book.pageNumber = 384
    app_book.image = 'images/books/book_17.jpg'
    app_book.isbn10 = '5-17-025476-8'
    app_book.isbn13 = '978-5-17-025476-7'
    app_book.description = '''
 На ночных улицах - опасно. Но речь не о преступниках и маньяках. На ночных улицах живет другая опасность - те, что называют себя Иными. Вампиры и оборотни, колдуньи и ведьмаки. Те, кто выходит на охоту, когда садится солнце. Те, чья сила велика, с кем не справиться обычным оружием. Но по следу "ночных охотников" веками следуют охотники другие - Ночной Дозор. Они сражаются с порождениями мрака и побеждают их, но при этом свято блюдут древний Договор, заключенный между Светлыми и Темными… '''

    app_book = importer.save_or_locate(app_book)

    offer = Offer()
    offer.updated = dateutil.parser.parse("2015-12-18T12:00:00.000000+00:00")
    offer.seller_user = User.objects.filter(email='andrej@andrej.in').first()
    offer.book = Book.objects.filter(name = 'Ночной Дозор').first()
    offer.price = 20
    offer.shipping_price = 3
    offer.active = True
    offer = importer.save_or_locate(offer)

    app_book = Book()
    app_book.user = User.objects.filter(email='andrej@andrej.in').first()
    app_book.name = 'Die Abenteuer des Stefón Rudel'
    app_book.author = 'Stefan Knapp'
    app_book.language = 'DE'
    app_book.releaseDate = dateutil.parser.parse("2004")
    app_book.pageNumber = 384
    app_book.image = 'images/books/book_18.jpg'
    app_book.isbn10 = '84-9015-648-4'
    app_book.isbn13 = '978-84-9015-648-3'
    app_book.description = '''
        Das Buch handelt von jungen Stefón Rudel der zahlreiche Abenteuer auf Menschheitsabsicherungsplattos erlebt.Der Autor Stefan Knapp hat auf einzig Art und Weise die Abenteuer des Stefón Rudel in einer Fantastischen Abenteuergeschichte zusammengefasst.'''
    app_book = importer.save_or_locate(app_book)

    offer = Offer()
    offer.updated = dateutil.parser.parse("2015-12-18T12:00:00.000000+00:00")
    offer.seller_user = User.objects.filter(email='andrej@andrej.in').first()
    offer.book = Book.objects.filter(name = 'Die Abenteuer des Stefón Rudel').first()
    offer.price = 1
    offer.shipping_price = 3
    offer.active = True
    offer = importer.save_or_locate(offer)

    app_book = Book()
    app_book.user = User.objects.filter(email='jens@book2.de').first()
    app_book.name = 'Die Expedition: In 13 Jahren um die Welt'
    app_book.author = 'Jason Lewis'
    app_book.language = 'DE'
    app_book.releaseDate = dateutil.parser.parse("2015")
    app_book.pageNumber = 912
    app_book.image = 'images/books/book_19.jpg'
    app_book.isbn10 = '38-9029-458-8'
    app_book.isbn13 = '978-38-9029-458-8'
    app_book.description = '''
        Im Pedalboot über den Atlantik und auf Inlineskates durch die USA, mit dem Fahrrad ins Outback und im Kajak auf den Nil: Genau 158 Monate und 23 Tage ist Jason Lewis unterwegs und erlebt vom Überfall durch Piraten bis hin zur Krokodilattacke alle Höhen und Tiefen einer außerordentlich intensiven Weltumrundung. Und trotz des brutalen Zusammenpralls mit einem Auto, einer Höhenerkrankung im Himalaja und Spionagevorwürfen im Sudan wird die bewegende Tour für den Ausnahmeabenteurer ein persönlicher Erfolg: Kann er doch an Hunderten Schulen junge Menschen mit seiner Idee von einer nachhaltigen gemeinsamen Zukunft begeistern. Eine der wohl längsten und inspirierendsten Reisen der Geschichte und ein Meilenstein des Genres in zwei attraktiven Bänden.'''
    app_book = importer.save_or_locate(app_book)

    offer = Offer()
    offer.updated = dateutil.parser.parse("2015-12-18T12:00:00.000000+00:00")
    offer.seller_user = User.objects.filter(email='jens@book2.de').first()
    offer.book = Book.objects.filter(name = 'Die Expedition: In 13 Jahren um die Welt').first()
    offer.price = 10
    offer.shipping_price = 3
    offer.active = True
    offer = importer.save_or_locate(offer)

    app_book = Book()
    app_book.user = User.objects.filter(email='jens@book2.de').first()
    app_book.name = 'Dachdecker wollte ich eh nicht werden: Das Leben aus der Rollstuhlperspektive'
    app_book.author = 'Raúl Aguayo-Krauthausen'
    app_book.language = 'DE'
    app_book.releaseDate = dateutil.parser.parse("2014")
    app_book.pageNumber = 256
    app_book.image = 'images/books/book_20.jpg'
    app_book.isbn10 = '34-9962-281-5'
    app_book.isbn13 = '978-34-9962-281-5'
    app_book.description = '''
        Ein persönliches Plädoyer für Toleranz und Freude am Leben Menschen tätscheln ihm den Kopf oder starren ihn an – Raúl Aguayo-Krauthausen, der aufgrund seiner Glasknochen im Rollstuhl sitzt und kleinwüchsig ist, weiß, dass viele Menschen Schwierigkeiten haben, mit Behinderten unverkrampft umzugehen. Dabei ist jeder zehnte Deutsche behindert, da sollten wir uns doch eigentlich an den Umgang mit jenen gewöhnt haben, die nicht «normal» sind. Doch das Gegenteil ist der Fall. Raúl Aguayo-Krauthausen sieht seine Behinderung als eine Eigenschaft von vielen. Er beschreibt mit Witz und Sachkenntnis, wie sein Alltag wirklich ist und wie ein Miteinander von behinderten und noch-nicht-behinderten Menschen aussehen kann. «Was soll denn an dieser Behinderung Besonderes sein? Raúl Krauthausen ist einfach ein sehr beeindruckender Mensch mit starken Gaben. Er hat viel zu sagen und sich über seinen Rollstuhl schon lange erhoben.» (Roger Willemsen)'''
    app_book = importer.save_or_locate(app_book)

    offer = Offer()
    offer.updated = dateutil.parser.parse("2015-12-18T12:00:00.000000+00:00")
    offer.seller_user = User.objects.filter(email='jens@book2.de').first()
    offer.book = Book.objects.filter(name = 'Dachdecker wollte ich eh nicht werden: Das Leben aus der Rollstuhlperspektive').first()
    offer.price = 5
    offer.shipping_price = 3
    offer.active = True
    offer = importer.save_or_locate(offer)

    app_book = Book()
    app_book.user = User.objects.filter(email='jens@book2.de').first()
    app_book.name = 'Die granulare Gesellschaft: Wie das Digitale unsere Wirklichkeit auflöst'
    app_book.author = 'Christoph Kucklick'
    app_book.language = 'DE'
    app_book.releaseDate = dateutil.parser.parse("2016")
    app_book.pageNumber = 272
    app_book.image = 'images/books/book_21.jpg'
    app_book.isbn10 = '35-4837-625-8'
    app_book.isbn13 = '978-35-4837-625-8'
    app_book.description = '''
        Die Digitalisierung verändert uns und unsere Welt fundamental: Die Differenz-Revolution vereinzelt die Menschen radikal und verstärkt die Ungleichheit. Die Intelligenz-Revolution mit der massenhaften Verbreitung intelligenter Maschinen führt zu einer Umverteilung von Wissen und Chancen – und ebenfalls zu stärkerer Ungleichheit. Müssen wir Menschen uns in Abgrenzung neu definieren als unberechenbare, spielerische und – im positiven Sinne – störende Wesen? Durch die Kontroll-Revolution werden wir nicht mehr ausgebeutet, sondern ausgedeutet und gefährden damit unsere Ideale wie Gerechtigkeit und Demokratie.'''
    app_book = importer.save_or_locate(app_book)

    offer = Offer()
    offer.updated = dateutil.parser.parse("2015-12-18T12:00:00.000000+00:00")
    offer.seller_user = User.objects.filter(email='jens@book2.de').first()
    offer.book = Book.objects.filter(name = 'Die granulare Gesellschaft: Wie das Digitale unsere Wirklichkeit auflöst').first()
    offer.price = 7
    offer.shipping_price = 3
    offer.active = True
    offer = importer.save_or_locate(offer)

    app_book = Book()
    app_book.user = User.objects.filter(email='jens@book2.de').first()
    app_book.name = 'Erkenne die Welt: Geschichte der Philosophie 1'
    app_book.author = 'Richard David Precht'
    app_book.language = 'DE'
    app_book.releaseDate = dateutil.parser.parse("2015")
    app_book.pageNumber = 576
    app_book.image = 'images/books/book_22.jpg'
    app_book.isbn10 = '34-4231-262-0'
    app_book.isbn13 = '978-34-4231-262-0'
    app_book.description = '''
        Richard David Precht erklärt uns in drei Bänden die großen Fragen, die sich die Menschen durch die Jahrhunderte gestellt haben. Im ersten Teil seiner auf drei Bände angelegten Geschichte der Philosophie beschreibt Richard David Precht die Entwicklung des abendländischen Denkens von der Antike bis zum Mittelalter. Kenntnisreich und detailliert verknüpft er die Linien der großen Menschheitsfragen und verfolgt die Entfaltung der wichtigsten Ideen – von den Ursprungsgefilden der abendländischen Philosophie an der schönen Küste Kleinasiens bis in die Klöster und Studierstuben, die Kirchen und Machtzentren des Spätmittelalters. Dabei bettet er die Philosophie in die politischen, wirtschaftlichen und sozialen Fragen der jeweiligen Zeit ein und macht sie auf diese Weise auch für eine größere Leserschaft lebendig. Ein Buch, das dazu hilft, sich einen tiefen Einblick in die Geschichte der Philosophie zu verschaffen und die Dinge zu ordnen. Tauchen Sie ein in die schier unerschöpfliche Fülle des Denkens!'''  
    app_book = importer.save_or_locate(app_book)
    
    offer = Offer()
    offer.updated = dateutil.parser.parse("2015-12-18T12:00:00.000000+00:00")
    offer.seller_user = User.objects.filter(email='jens@book2.de').first()
    offer.book = Book.objects.filter(name = 'Erkenne die Welt: Geschichte der Philosophie 1').first()
    offer.price = 8
    offer.shipping_price = 3
    offer.active = True
    offer = importer.save_or_locate(offer)

    app_book = Book()
    app_book.user = User.objects.filter(email='s0535844@htw-berlin.de').first()
    app_book.name = 'Der Dunkle Turm, Band 1: Schwarz'
    app_book.author = 'Steven King'
    app_book.language = 'DE'
    app_book.releaseDate = dateutil.parser.parse("2003-12-01")
    app_book.pageNumber = 352
    app_book.image = 'images/books/book_23.jpg'
    app_book.isbn10 = '34-5387-556-7'
    app_book.isbn13 = '978-34-5387-556-2'
    app_book.description = '''
        Im ersten Band von Stephen Kings epischer Fantasyserie durchstreift Roland, der letzte Revolvermann, auf der Suche nach dem mysteriösen Dunklen Turm eine sterbende Welt. Der Auftakt zur großen Saga jetzt in einer von Stephen King komplett überarbeiteten Fassung mit neuem Vorwort und neuer Einführung.'''
    app_book = importer.save_or_locate(app_book)

    offer = Offer()
    offer.updated = dateutil.parser.parse("2015-12-18T12:00:00.000000+00:00")
    offer.seller_user = User.objects.filter(email='s0535844@htw-berlin.de').first()
    offer.book = Book.objects.filter(name = 'Der Dunkle Turm, Band 1: Schwarz').first()
    offer.price = 5
    offer.shipping_price = 3
    offer.active = True
    offer = importer.save_or_locate(offer)
      
    app_book = Book()
    app_book.user = User.objects.filter(email='s0535844@htw-berlin.de').first()
    app_book.name = '365 Sexstellungen: Heiße Sexspiele für ein ganzes Jahr'
    app_book.author = 'Randi Foxx'
    app_book.language = 'DE'
    app_book.releaseDate = dateutil.parser.parse("2014-06-21")
    app_book.pageNumber = 352
    app_book.image = 'images/books/book_24.jpg'
    app_book.isbn10 = '38-0943-322-5'
    app_book.isbn13 = '978-38-0943-322-4'
    app_book.description = '''
        Spaß im Bett, und das an jedem Tag des Jahres. Abenteuerlustige Paare können hier die 365 heißesten Sexstellungen erproben. Wie wärs zum Start mit dem "Schlitten"? Aber auch die "Windmühle" und der "Ponyritt" lassen keine Langeweile aufkommen. Und zum krönenden Höhepunkt können Sie in einer "endlosen Umarmung" verschmelzen …'''
    app_book = importer.save_or_locate(app_book)

        
    offer = Offer()
    offer.updated = dateutil.parser.parse("2015-12-18T12:00:00.000000+00:00")
    offer.seller_user = User.objects.filter(email='s0535844@htw-berlin.de').first()
    offer.book = Book.objects.filter(name = '365 Sexstellungen: Heiße Sexspiele für ein ganzes Jahr').first()
    offer.price = 5
    offer.shipping_price = 3
    offer.active = True
    offer = importer.save_or_locate(offer)