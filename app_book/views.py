from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .models import Book, Offer
from app_user.models import User
from .forms import BookForm, OfferForm
from app_user.forms import RegistrationForm

import watson

# Custom Ownership Decorator
def owns_book(func):
    def check_and_call(request, *args, **kwargs):
        id = kwargs.get("id")
        if id == None:
            return func(request, *args, **kwargs)
        book = get_object_or_404(Book, id=id)
        if not (book.user.id == request.user.id):
            messages.add_message(request, messages.ERROR, 'Dies ist nicht Ihr Buch!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return func(request, *args, **kwargs)
    return check_and_call

@owns_book
def showEditBook(request, id, offerEnabled):
    template_name = 'app_book/archives_edit.html'

    if id is not None:
        book = Book.objects.get(pk=id)
        book_form = BookForm(instance=book)
        offer = book.offer_set.first()
        offer_form = OfferForm(instance=offer)
    else:
        book_form = BookForm()
        offer_form = OfferForm()

    if offerEnabled is None:
        offer_form.initial['offer_form_checkbox'] = (True if offer is not None else False)
    else:
        offer_form.initial['offer_form_checkbox'] = offerEnabled

    return render_to_response(template_name, {
        "form": book_form,
        "offer_form": offer_form,
    }, RequestContext(request))

@owns_book
def handleEditBook(request, id):
    if request.method == 'POST':

        if id is not None:
            book = Book.objects.get(pk=id)
            offer = book.offer_set.first()

            book_form = BookForm(request.POST, instance=book)
            offer_form = OfferForm(request.POST, instance=offer)

        else:
            book_form = BookForm(request.POST)
            offer_form = OfferForm(request.POST)

        try:
            if id is not None:
                book_form_obj = book_form.save()
            else:
                book_form_obj = book_form.save(commit=False)
                book_form_obj.user_id = request.user.id
                book_form_obj.save()

            if 'offer_form_checkbox' in request.POST and request.POST['offer_form_checkbox']:
                offer_form_obj = offer_form.save(commit=False)

                # reseting id and seller_user_id in case this will be a new offer
                offer_form_obj.id = book_form_obj.id
                offer_form_obj.seller_user_id = book_form_obj.user_id
                offer_form_obj.active = True
                offer_form_obj.save()
            return True

        except ValueError as e:
            print(e)

    return False


def archivesPageView(request):
    '''
    Diese Methode zeigt alle vorhandenen Buecher an
    :param request: Der Request der erzeugt wurde
    :return: allBooks: Alle Buecher
    '''
    template_name = 'app_book/archives.html'
    allBooks = Book.objects.filter(user = request.user);

    return render_to_response(template_name, {
        "allBooks": allBooks,
    }, RequestContext(request))


@owns_book
def archivesEditPageView(request, id):
    '''
    Diese Methode aktualisiert ein Buch
    :param request:  Request der gesendet wurde
    :param id: Buch ID welche aktualisiert werden soll
    :return:form: Die Form die aus dem Model generiert wird
    '''

    if request.method == 'POST':
        ret_val = handleEditBook(request, id)

        if ret_val:
            messages.add_message(request, messages.SUCCESS, 'Das Buch wurde erfolgreich aktualisiert!')
            return HttpResponseRedirect(reverse('app_book:archivesPage'))
        else:
            messages.add_message(request, messages.ERROR, 'Das Buch konnte leider nicht aktualisiert werden!')

    return showEditBook(request, id, None)

# Create your views here.
def archivesPageView(request):
    '''
    Diese Methode zeigt alle vorhandenen Buecher an und ermoeglicht es ein neues Buch zu speichern
    :param request: Der Request der erzeugt wurde
    :return: form: Die Form die sich generiert aus dem Model, collapsed: Status ob "Neues Buch hinzufuegen" angezeigt werden soll
    allBooks: Alle Buecher
    '''
    template_name = 'app_book/archives.html'
    collapsed = False

    if request.method == 'POST':
        try:
            form = BookForm(request.POST)
            form.save()
            collapsed = True
            messages.add_message(request, messages.SUCCESS, 'Das Buch wurde erfolgreich angelegt!')
        except ValueError as e:
            messages.add_message(request, messages.ERROR, 'Das Buch konnte leider nicht gespeichert werden!')
    else:
        form = BookForm()
        collapsed = True

    allBooks = Book.objects.filter(user = request.user);

    return render_to_response(template_name, {
        "form": form,
        "collapsed": collapsed,
        "allBooks": allBooks,
    },  RequestContext(request))

@owns_book
def archivesEditPageView(request, id):
    '''
    Diese Methode aktualisiert ein Buch
    :param request:  Request dder gesendet wurde
    :param id: Buch ID welches aktualisiert werden soll
    :return:form: Die Form die generiert wird aus dem Model
    '''
    template_name = 'app_book/archives_edit.html'
    book = Book.objects.get(pk=id);
    form = BookForm(instance=book)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        try:
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Das Buch wurde erfolgreich aktualisiert!')
            return HttpResponseRedirect(reverse('app_book:archivesPage'))
        except ValueError as e:
            messages.add_message(request, messages.ERROR, 'Das Buch konnte leider nicht aktualisiert werden!')
    return render_to_response(template_name, {
        "form": form,
        "book": book,
    },  RequestContext(request))


@owns_book
def deleteBook(request, id):
    if request.method == 'DELETE':
        book = get_object_or_404(Book, id=id)
        book.delete()
        messages.add_message(request, messages.SUCCESS, 'Das Buch wurde erfolgreich gelöscht!')
        # use GET request for redirected location via HTTP status code 303 (see other).
        return HttpResponseRedirect(reverse('app_book:archivesPage'), status=303)
    else:
        raise BaseException("Use http method DELETE for deleting a book.")

def searchBook(request):
    template_name = 'app_book/search.html'

    return render_to_response(template_name, {
    },  RequestContext(request))

def searchBookResults(request):
    template_name = 'app_book/search_result.html'
    if request.method == 'GET':
        if not request.GET.get("search_string", ""):
            return HttpResponseRedirect(reverse('app_book:searchBook'), status=303)
        search_string = request.GET.get("search_string", "")
        search_results = watson.search(search_string, exclude=(Book.objects.filter(offer__lte = 0)))

    return render_to_response(template_name, {
        "results": search_results,
    },  RequestContext(request))


def createBook(request):
    if request.method == 'POST':
        ret_val = handleEditBook(request, None)

        if ret_val:
            messages.add_message(request, messages.SUCCESS, 'Das Buch wurde erfolgreich angelegt!')
            return HttpResponseRedirect(reverse('archivesPage'))
        else:
            messages.add_message(request, messages.ERROR, 'Das Buch konnte leider nicht angelegt werden!')

    return showEditBook(request, None, False)


@owns_book
def publishBook(request, id):
    if request.method == 'POST':
        ret_val = handleEditBook(request, id)

        if ret_val:
            messages.add_message(request, messages.SUCCESS, 'Das Buch wurde erfolgreich aktualisiert und nun zum Verkauf angeboten!')
            return HttpResponseRedirect(reverse('app_book:showcase', kwargs={'user_id': request.user.id}), status=303)
        else:
            messages.add_message(request, messages.ERROR, 'Das Buch konnte leider nicht aktualisiert werden!')

    return showEditBook(request, id, True)


@owns_book
def unpublishBook(request, id):
    if request.method == 'PUT':
        book = get_object_or_404(Book, id=id)
        offer = book.offer_set.first()
        if offer is not None:
            offer.active = False
            offer.save()
        messages.add_message(request, messages.SUCCESS, 'Das Buch wird nun nicht mehr zum Verkauf angeboten!')
        # use GET request for redirected location via HTTP status code 303 (see other).
        return HttpResponseRedirect(reverse('app_book:showcase', kwargs={'user_id': book.user_id}), status=303)
    else:
        raise ("Use http method PUT for unpublishing a book.")


def showcaseView(request, user_id):
    template_name = 'app_book/showcase.html'

    user = User.objects.filter(pk=user_id).first()

    offers = Offer.objects.filter(seller_user_id=user_id, active=True).all()
    bookIds = offers.values_list('book', flat=True)
    books = Book.objects.filter(id__in=bookIds).all()

    return render_to_response(template_name, {
        "user": user,
        "offers": offers,
        "books": books,
    }, RequestContext(request))
