# coding=utf-8

import datetime

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
import watson

from .models import User, Book, Offer
from .forms import BookForm
from .forms import RegistrationForm

class StartPageView(TemplateView):
    template_name = 'app/start.html'

    def get_context_data(self, **kwargs):
        context = super(StartPageView, self).get_context_data(**kwargs)
        return context

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Sie haben sich erfolgreich registriert.')
            return HttpResponseRedirect(reverse('startPage'))
    else:
        form = RegistrationForm()
    return render_to_response('app/register.html', {'form': form}, RequestContext(request))

def archivesPageView(request):
    '''
    Diese Methode zeigt alle vorhandenen Buecher an und ermoeglicht es ein neues Buch zu speichern
    :param request: Der Request der erzeugt wurde
    :return: form: Die Form die sich generiert aus dem Model, collapsed: Status ob "Neues Buch hinzufuegen" angezeigt werden soll
    allBooks: Alle Buecher
    '''
    template_name = 'app/archives.html'
    collapsed = False

    if request.method == 'POST':
        try:
            form = BookForm(request.POST)

            formObject = form.save(commit=False)
            formObject.user_id = request.user.id
            formObject.save()

            collapsed = True
            messages.add_message(request, messages.SUCCESS, 'Das Buch wurde erfolgreich angelegt!')
        except ValueError as e:
            print(e)
            messages.add_message(request, messages.ERROR, 'Das Buch konnte leider nicht gespeichert werden!')
    else:
        form = BookForm()
        collapsed = True

    allBooks = Book.objects.all();

    return render_to_response(template_name, {
        "form": form,
        "collapsed": collapsed,
        "allBooks": allBooks,
    },  RequestContext(request))

def archivesEditPageView(request, book_id):
    '''
    Diese Methode aktualisiert ein Buch
    :param request:  Request dder gesendet wurde
    :param book_id: Buch ID welches aktualisiert werden soll
    :return:form: Die Form die generiert wird aus dem Model
    '''
    template_name = 'app/archives_edit.html'
    book = Book.objects.get(pk=book_id);
    form = BookForm(instance=book)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        try:
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Das Buch wurde erfolgreich aktualisiert!')
            return HttpResponseRedirect(reverse('archivesPage'))
        except ValueError as e:
            messages.add_message(request, messages.ERROR, 'Das Buch konnte leider nicht aktualisiert werden!')
    return render_to_response(template_name, {
        "form": form,
        "book": book,
    },  RequestContext(request))


def deleteBook(request, id):
    if request.method == 'DELETE':
        book = get_object_or_404(Book, id=id)
        book.delete()
        messages.add_message(request, messages.SUCCESS, 'Das Buch wurde erfolgreich gelöscht!')
        # use GET request for redirected location via HTTP status code 303 (see other).
        return HttpResponseRedirect(reverse('archivesPage'), status=303)
    else:
        raise BaseException("Use http method DELETE for deleting a book.")

def searchBook(request):
    template_name = 'app/search.html'

    return render_to_response(template_name, {
    },  RequestContext(request))

def searchBookResults(request):
    template_name = 'app/search_result.html'
    if request.method == 'GET':
        if not request.GET.get("search_string", ""):
            return HttpResponseRedirect(reverse('searchBook'), status=303)
        print("search string: "+request.GET.get("search_string", ""))
        search_results = watson.search(request.GET.get("search_string", ""))

    return render_to_response(template_name, {
        "results": search_results,
    },  RequestContext(request))


def publishBook(request, id):
    if request.method == 'PUT':
        book = get_object_or_404(Book, id=id)

        offer = Offer(seller_user_id=request.user.id, book=book, price=12.0, shipping_price=10.00)
        offer.save()

        messages.add_message(request, messages.SUCCESS, 'Das Buch wird nun zum Verkauf angeboten!')
        # use GET request for redirected location via HTTP status code 303 (see other).
        return HttpResponseRedirect(reverse('user-showcase', kwargs={'user_id': book.user_id}), status=303)
    else:
        raise("Use http method PUT for publishing a book.")


def unpublishBook(request, id):
    if request.method == 'PUT':
        book = get_object_or_404(Book, id=id)
        book.releaseDate = "2015-01-01"
        book.save()
        messages.add_message(request, messages.SUCCESS, 'Das Buch wird nun nicht mehr zum Verkauf angeboten!')
        # use GET request for redirected location via HTTP status code 303 (see other).
        return HttpResponseRedirect(reverse('user-showcase', kwargs={'user_id': book.user_id}), status=303)
    else:
        raise("Use http method PUT for unpublishing a book.")


def showcaseView(request, user_id):
    template_name = 'app/showcase.html'



    user = User.objects.filter(pk=user_id).first()

    offers = Offer.objects.filter(seller_user_id=user_id).all()
    bookIds = offers.values_list('book', flat=True)
    books = list( Book.objects.filter( id__in=bookIds ).all() )

    return render_to_response( template_name, {
        "user":   user,
        "offers": offers,
        "books":  books,
    },  RequestContext(request))
