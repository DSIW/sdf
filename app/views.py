from _testcapi import instancemethod
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.forms.models import modelformset_factory
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .forms import NewBookForm
from .models import Book

class StartPageView(TemplateView):
    template_name = 'app/start.html'

    def get_context_data(self, **kwargs):
        context = super(StartPageView, self).get_context_data(**kwargs)
        return context


def archivesPageView(request):
    '''
    Diese Methode zeigt alle vorhandenen Buecher an und ermoeglicht es ein neues Buch zu speichern
    :param request: Der Request der erzeugt wurde
    :return: formset: Die Form die sich generiert aus dem Model, collapsed: Status ob "Neues Buch hinzufuegen" angezeigt werden soll
    allSavedCustomerBooks: Alle gespeicherten Buecher
    '''
    template_name = 'app/archives.html'
    collapsed = False

    newBookFormSet = modelformset_factory(Book, NewBookForm)
    if request.method == 'POST':
        try:
            formset = newBookFormSet(request.POST)
            NewBookForm.validateAndSaveNewBook(formset)
            formset = newBookFormSet(queryset=Book.objects.none())
            collapsed = True
            messages.add_message(request, messages.SUCCESS, 'Das Buch wurde erfolgreich angelegt!')
        except ValidationError as e:
            messages.add_message(request, messages.ERROR, 'Das Buch konnte leider nicht gespeichert werden!')
    else:
        formset = newBookFormSet(queryset=Book.objects.none())
        collapsed = True

    allSavedCustomerBooks=Book.objects.all();



    return render_to_response(template_name, {
        "formset": formset,
        "collapsed": collapsed,
        "allSavedCustomerBooks": allSavedCustomerBooks,
    },  RequestContext(request))

def archivesEditPageView(request, book_id):
    '''
    Diese Methode aktualisiert ein Buch
    :param request:  Request dder gesendet wurde
    :param book_id: Buch ID welches aktualisiert werden soll
    :return:formset: Die Form die generiert wird aus dem Model
    '''
    template_name = 'app/archives_edit.html'
    bookEdit = Book.objects.get(pk=book_id);
    editBookFormSet = NewBookForm(instance=bookEdit)

    if request.method == 'POST':
        try:
            formset = NewBookForm(request.POST, instance=Book.objects.get(pk=book_id))
            NewBookForm.validateAndUpateBook(formset)
            messages.add_message(request, messages.SUCCESS, 'Das Buch wurde erfolgreich aktualisiert!')
        except ValidationError as e:
            messages.add_message(request, messages.ERROR, 'Das Buch konnte leider nicht aktualisiert werden!')

    return render_to_response(template_name, {
        "formset": editBookFormSet,
        "book": bookEdit,
    },  RequestContext(request))

def deleteBook(request, id):
    if request.method == 'DELETE':
        book = get_object_or_404(Book, id=id)
        book.delete()
        messages.add_message(request, messages.SUCCESS, 'Das Buch wurde erfolgreich gelöscht!')
        # use GET request for redirected location via HTTP status code 303 (see other).
        return HttpResponseRedirect(reverse('archivesPage'), status=303)
    else:
        raise("Use http method DELETE for deleting a book.")

