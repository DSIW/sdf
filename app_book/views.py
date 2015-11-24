from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db import IntegrityError

import watson
import collections

from app_user.models import User
from app_user.forms import RegistrationForm

from .models import Book, Offer
from .forms import BookForm, OfferForm, PublishOfferForm


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


StatusAndTwoForms = collections.namedtuple("StatusAndTwoForms", ["status", "form_one", "form_two"], verbose=False, rename=False)


@owns_book
def showEditBook(request, id, offer_enabled):
    offer = None
    book_form = BookForm()
    offer_form = OfferForm()

    if id is not None:
        book = Book.objects.get(pk=id)
        offer = book.offer_set.first()
        book_form = BookForm(instance=book)
        offer_form = OfferForm(instance=offer)

    if offer_enabled is not None:
        offer_form.initial['id_active'] = offer_enabled
    else:
        offer_form.initial['id_active'] = (offer is not None)

    return StatusAndTwoForms(True, book_form, offer_form)

@owns_book
def handleEditBook(request, id):
    if request.method != 'POST':
        return StatusAndTwoForms(False, None, None)

    book = None
    offer = None

    if id is not None:
        book = Book.objects.get(pk=id)
        offer = book.offer_set.first()

    book_form = BookForm(request.POST, instance=book)
    offer_form = OfferForm(request.POST, instance=offer)

    if not book_form.is_valid():
        return StatusAndTwoForms(False, book_form, offer_form)
    try:
        if id is None:
            book_form_obj = book_form.save(commit=False)
            book_form_obj.user_id = request.user.id
            book_form_obj.save()
        else:
            book_form_obj = book_form.save()
    except ValueError as e:
        return StatusAndTwoForms(False, book_form, offer_form)

    if 'active' in request.POST and request.POST['active']:
        if not offer_form.is_valid():
            return StatusAndTwoForms(False, book_form, offer_form)
        offer_form_obj = offer_form.save(commit=False)
        # reseting id and seller_user_id in case this will be a new offer
        offer_form_obj.id = book_form_obj.id
        offer_form_obj.seller_user_id = book_form_obj.user_id
        try:
            offer_form_obj.save()
            return StatusAndTwoForms(True, None, None)
        except ValueError as e:
            return StatusAndTwoForms(False, book_form, offer_form)
    elif offer is not None:
        try:
            # TODO: hack(ish) find better solution
            Offer.objects.filter(pk=offer.id).update(active=False)
        except ValueError as e:
            return StatusAndTwoForms(False, book_form, offer_form)

    return StatusAndTwoForms(True, None, None)


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
def editBook(request, id):
    if request.method == 'POST':
        ret_val = handleEditBook(request, id)

        if ret_val.status:
            messages.add_message(request, messages.SUCCESS, 'Das Buch wurde erfolgreich aktualisiert!')
            return HttpResponseRedirect(reverse('app_book:archivesPage'))
        else:
            messages.add_message(request, messages.ERROR, 'Das Buch konnte leider nicht aktualisiert werden!')
    else:
        ret_val = showEditBook(request, id, None)

    return render_to_response('app_book/edit_book.html', {
        "book_form": ret_val.form_one,
        "offer_form": ret_val.form_two,
    }, RequestContext(request))


def showcaseView(request, user_id):
    template_name = 'app_book/showcase.html'

    user = get_object_or_404(User, id=user_id)
    offers = Offer.objects.filter(seller_user_id=user_id, active=True).all()

    return render_to_response(template_name, {
        "user": user,
        "offers": offers,
    }, RequestContext(request))


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


def createBook(request):
    if request.method == 'POST':
        ret_val = handleEditBook(request, None)

        if ret_val.status:
            messages.add_message(request, messages.SUCCESS, 'Das Buch wurde erfolgreich angelegt!')
            return HttpResponseRedirect(reverse('app_book:archivesPage'))
        else:
            messages.add_message(request, messages.ERROR, 'Das Buch konnte leider nicht angelegt werden!')
    else:
        ret_val = showEditBook(request, None, False)

    return render_to_response('app_book/edit_book.html', {
        "book_form": ret_val.form_one,
        "offer_form": ret_val.form_two,
    }, RequestContext(request))


@owns_book
def publishBook(request, id):
    book = get_object_or_404(Book, id=id)
    offer = book.offer_set.first()
    offer_form = PublishOfferForm(instance=offer)

    if request.method == 'POST':
        offer_form = PublishOfferForm(request.POST, instance=offer)

        if offer_form.is_valid():
            offer_form_obj = offer_form.save(commit=False)
            offer_form_obj.active = True
            offer_form_obj.book_id = id
            offer_form_obj.seller_user_id = book.user_id

            try:
                offer_form_obj.save()
                messages.add_message(request, messages.SUCCESS, 'Das Buch wird nun zum Verkauf angeboten!')
                return HttpResponseRedirect(reverse('app_book:archivesPage'))
            except ValueError as e:
                messages.add_message(request, messages.ERROR, 'Das Buch konnte leider nicht zum Verkauf angeboten werden!')

    return render_to_response('app_book/publish_book.html', {
        "offer_form": offer_form,
        "book": book,
    }, RequestContext(request))


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
        return HttpResponseRedirect(reverse('app_book:archivesPage'))
    else:
        raise ("Use http method PUT for unpublishing a book.")


def searchBookResults(request):
    template_name = 'app_book/search_result.html'
    search_results = watson.search(request.GET.get("search_string", ""))

    return render_to_response(template_name, {
        "results": search_results,
    },  RequestContext(request))

