# -*- coding: utf-8 -*-
import operator
from functools import reduce

import collections

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db import IntegrityError
from django.utils.html import escape
from django.http import JsonResponse

from app_payment.services import start_payment
from .models import Book
from .forms import BookForm
from sdf import settings

import watson
import collections

from app_user.models import User
from app_payment.models import SellerRating, Payment
from app_notification.models import Notification

from .models import Book, Offer, Counteroffer
from .forms import BookForm, OfferForm, PublishOfferForm, CounterofferForm
from .services import unpublish_book
from app_payment.views import build_payment_form

StatusAndTwoForms = collections.namedtuple("StatusAndTwoForms", ["status", "form_one", "form_two"], verbose=False,
                                           rename=False)

# Custom Ownership Decorator
def can_show_book(func):
    def check_and_call(request, *args, **kwargs):
        id = kwargs.get("id")
        if id == None:
            return func(request, *args, **kwargs)
        book = get_object_or_404(Book, id=id)
        if book.is_private() and not (book.user.id == request.user.id):
            messages.add_message(request, messages.ERROR, 'Sie haben keine Berechtigung das Buch anzusehen!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return func(request, *args, **kwargs)
    return check_and_call


def can_change_book(func):
    def check_and_call(request, *args, **kwargs):
        id = kwargs.get("id")
        if id == None:
            return func(request, *args, **kwargs)
        book = get_object_or_404(Book, id=id)
        if not (book.user.id == request.user.id):
            messages.add_message(request, messages.ERROR, 'Sie haben keine Berechtigung das Buch anzusehen!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return func(request, *args, **kwargs)
    return check_and_call


@can_change_book
def showEditBook(request, id, offer_enabled):
    if id is not None:
        book = Book.objects.get(pk=id)
        offer = book.offer_set.first()
        book_form = BookForm(instance=book)
        offer_form = OfferForm(instance=offer)
    else:
        offer = None
        book_form = BookForm()
        offer_form = OfferForm()


    if offer_enabled is not None:
        offer_form.initial['id_active'] = offer_enabled
    else:
        offer_form.initial['id_active'] = (offer is not None)

    return StatusAndTwoForms(True, book_form, offer_form)


@can_change_book
@login_required
@transaction.atomic
def handleEditBook(request, id):
    if request.method != 'POST':
        return StatusAndTwoForms(False, None, None)

    # TODO check: do all browsers send checkbox status strings as {on|off} ?
    offer_active = ('active' in request.POST and request.POST['active'] == 'on')
    book = None
    offer = None

    if id is not None:
        book = Book.objects.get(pk=id)
        offer = book.offer_set.first()

    book_form = BookForm(request.POST, request.FILES, instance=book)
    offer_form = OfferForm(request.POST, instance=offer)

    # check validity of forms
    if (not book_form.is_valid()) or (offer_active and not offer_form.is_valid()):
        if book_form.errors and 'image' in book_form.errors.keys():
            # Workaround for showing existing cover image instead of broken result
            old_errors = book_form._errors
            if book:
                original_book = Book.objects.get(pk=book.id)
                book.image = original_book.image
            files = {}
            files.update(request.FILES)
            if 'image' in files.keys(): del files['image']
            book_form = BookForm(request.POST, files, instance=book)
            book_form._errors = old_errors
        return StatusAndTwoForms(False, book_form, offer_form)

    try:
        with transaction.atomic():
            if id is None:
                book_form_obj = book_form.save(commit=False)
                book_form_obj.user_id = request.user.id
                book_form_obj.save()
            elif ('delete_saved_image' in request.POST and request.POST['delete_saved_image'] == 'on'):
                book_form_obj = book_form.save(commit=False)
                book_form_obj.image = None
                book_form_obj.save()
            else:
                book_form_obj = book_form.save()

            # handle offer
            if offer_active:
                offer_form_obj = offer_form.save(commit=False)
                # reseting id and seller_user_id in case this will be a new offer
                offer_form_obj.book_id = book_form_obj.id
                offer_form_obj.seller_user_id = book_form_obj.user_id
                offer_form_obj.save()

            # disable existing offer if form active is false
            elif offer is not None:
                # TODO: hack(ish) find better solution
                Offer.objects.filter(pk=offer.id).update(active=False)

            return StatusAndTwoForms(True, book_form, offer_form)

    except ValueError as e:
        return StatusAndTwoForms(False, book_form, offer_form)


@login_required
def archivesPageView(request):
    '''
    Diese Methode zeigt alle vorhandenen Buecher an
    :param request: Der Request der erzeugt wurde
    :return: allBooks: Alle Buecher
    '''
    template_name = 'app_book/archives.html'
    allBooks = Book.objects.filter(user=request.user);

    return render_to_response(template_name, {
        "allBooks": allBooks,
    }, RequestContext(request))


@can_show_book
def detailView(request, id):
    template_name = 'app_book/detail.html'

    book = get_object_or_404(Book, id=id)
    payment = book.active_payment()

    return render_to_response(template_name, {
        "book": book,
        "payment_form": build_payment_form(payment)
    },  RequestContext(request))


@login_required
@can_change_book
def editBook(request, id):
    if request.method == 'POST':
        ret_val = handleEditBook(request, id)

        if ret_val.status:
            messages.add_message(request, messages.SUCCESS, 'Das Buch wurde erfolgreich aktualisiert!')
            return HttpResponseRedirect(reverse('app_book:book-detail', kwargs={'id': id}))
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
        "showcase_user": user,
        "offers": offers,
    }, RequestContext(request))


@login_required
@can_change_book
def deleteBook(request, id):
    if request.method == 'DELETE':
        book = get_object_or_404(Book, id=id)
        book.delete()
        messages.add_message(request, messages.SUCCESS, 'Das Buch wurde erfolgreich gelöscht!')
        # use GET request for redirected location via HTTP status code 303 (see other).
        return HttpResponseRedirect(reverse('app_book:archivesPage'), status=303)
    else:
        raise BaseException("Use http method DELETE for deleting a book.")


@login_required
def createBook(request):
    if request.method == 'POST':
        ret_val = handleEditBook(request, None)

        if ret_val.status:
            messages.add_message(request, messages.SUCCESS, 'Das Buch wurde erfolgreich angelegt!')
            return HttpResponseRedirect(reverse('app_book:book-detail', kwargs={'id': ret_val.form_one.instance.id}))
        else:
            messages.add_message(request, messages.ERROR, 'Das Buch konnte leider nicht angelegt werden!')
    else:
        ret_val = showEditBook(request, None, False)

    return render_to_response('app_book/edit_book.html', {
        "book_form": ret_val.form_one,
        "offer_form": ret_val.form_two,
    }, RequestContext(request))


@login_required
@can_change_book
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
                messages.add_message(request, messages.ERROR,
                                     'Das Buch konnte leider nicht zum Verkauf angeboten werden!')

    return render_to_response('app_book/publish_book.html', {
        "offer_form": offer_form,
        "book": book,
    }, RequestContext(request))


@login_required
@can_change_book
def unpublishBook(request, id):
    if request.method == 'PUT':
        book = get_object_or_404(Book, id=id)
        unpublish_book(book)
        messages.add_message(request, messages.SUCCESS, 'Das Buch wird nun nicht mehr zum Verkauf angeboten!')
        # decline all active counteroffers:
        offer = book.offer_set.first()
        counteroffers = Counteroffer.objects.filter(offer=offer, active=True)
        for co in counteroffers:
            Notification.counteroffer_decline(co, co.creator, book)
        # use GET request for redirected location via HTTP status code 303 (see other).

        counteroffers.update(active=False, accepted=False)
        return HttpResponseRedirect(reverse('app_book:archivesPage'))
    else:
        raise ("Use http method PUT for unpublishing a book.")


@login_required
def counteroffer(request, id):
    offer = get_object_or_404(Offer, id=id)
    user = get_object_or_404(User, id=request.user.id)
    book = get_object_or_404(Book, id=offer.book.id)

    if not offer.allow_counteroffers:
        messages.add_message(request, messages.ERROR, 'Der Verkäufer erlaubt keine Preisvorschläge!')
        return HttpResponseRedirect(reverse('app_book:book-detail', kwargs = {'id': book.id}))

    counter_offer = Counteroffer(offer=offer, creator=user, price=offer.totalPrice(), active=True, accepted=False)
    offer_form = CounterofferForm(instance=counter_offer)
    if request.method == 'GET':
        return render_to_response('app_book/_counteroffer_form.html', {
            "form": offer_form,
            "offer": offer,
            "book": book,
        }, RequestContext(request))
    if request.method == 'POST':
        offer_form = CounterofferForm(request.POST, instance=counter_offer)
        if offer_form.is_valid():
            counter_offer = offer_form.save(commit=False)
            counter_offer.save()
            messages.add_message(request, messages.SUCCESS,
                    'Der Preisvorschlag wurde abgegeben. Sie werden benachrichtigt, sobald der Verkäufer antwortet')
            offer.counteroffer_set.add(counter_offer);
            offer.save()

            seller = get_object_or_404(User, id=offer.seller_user.id)
            Notification.counteroffer(counter_offer, seller, user, book)
        else:
            return render_to_response('app_book/_counteroffer_form.html', {
                "form": offer_form,
                "offer": offer,
                "book": book,
            }, RequestContext(request))
    else:
        raise ("Use http method POST for making a counteroffer")

    return HttpResponseRedirect(reverse('app_book:book-detail', kwargs = {'id': book.id}))


@login_required
def accept_counteroffer(request, id):
    counteroffer = get_object_or_404(Counteroffer, id=id)
    buyer = get_object_or_404(User, id=counteroffer.creator.id)
    offer = get_object_or_404(Offer, id=counteroffer.offer.id)
    book = get_object_or_404(Book, id=offer.book.id)

    counteroffer.accept()

    # Erstelle Paypalpayment, sodass für das Buch keine Vorschläge mehr abgegeben werden können
    payment = book.active_payment()
    if payment is None:
        payment = Payment()
    success = start_payment(payment, offer, buyer, 'counteroffer')
    if success:
        payment.amount = counteroffer.price
        payment.save()

        # hide book
        offer.active = False
        offer.save()

        Notification.counteroffer_accept(counteroffer, buyer, book, payment)
        messages.add_message(request, messages.SUCCESS, 'Der Preisvorschlag wurde erfolgreich angenommen. Der Interessent wird benachrichtigt')

    return HttpResponseRedirect(reverse('app_notification:notificationsPage'))


@login_required
def decline_counteroffer(request, id):
    counteroffer = get_object_or_404(Counteroffer, id=id)
    buyer = get_object_or_404(User, id=counteroffer.creator.id)
    offer = get_object_or_404(Offer, id=counteroffer.offer.id)
    book = get_object_or_404(Book, id=offer.book.id)

    # Akzeptiere nicht
    Notification.counteroffer_decline(counteroffer, buyer, book)
    counteroffer.decline()
    messages.add_message(request, messages.SUCCESS,
                         'Der Preisvorschlag wurde erfolgreich abgelehnt. Der Interessent wird benachrichtigt')

    return HttpResponseRedirect(reverse('app_notification:notificationsPage'))

def filter_books(search_string):
    filtered_books = watson.search(search_string,models=(Book,))
    for book in filtered_books:
        yield book.object.offer_set.first()

def books(request):
    template_name = 'app_book/books.html'
    filtered_offers = []

    search_string = escape(request.GET.get('search_string', ''))

    if search_string:
        filtered_offers.extend(filter_books(search_string))
    else:
        filtered_offers.extend(Offer.objects.filter(active=True))

    page = request.GET.get('page')
    order_by = request.GET.get('order_by', 'date')
    order_dir = request.GET.get('order_dir', 'desc')
    order_dir_is_desc = order_dir == 'desc'

    if order_by == 'date':
        filtered_offers.sort(key=lambda offer: offer.updated, reverse=order_dir_is_desc)
    elif order_by == 'title':
        filtered_offers.sort(key=lambda offer: offer.book.name.lower(), reverse=order_dir_is_desc)
    elif order_by == 'author':
        filtered_offers.sort(key=lambda offer: offer.book.author.lower(), reverse=order_dir_is_desc)
    elif order_by == 'price':
        filtered_offers.sort(key=lambda offer: (offer.price + offer.shipping_price), reverse=order_dir_is_desc)
    else:
        filtered_offers.sort(key=lambda offer: offer.updated, reverse=order_dir_is_desc)

    paginator = Paginator(filtered_offers, settings.MAX_ELEMENTS_PER_PAGE)

    try:
        offers = paginator.page(page)
    except PageNotAnInteger:
        offers = paginator.page(1)
    except EmptyPage:
        offers = paginator.page(paginator.num_pages)

    return render_to_response(template_name, {
        "offers": offers,
        "order_by": order_by,
        "order_dir": order_dir,
        "request": request,
    }, RequestContext(request))


def filter_users_with_offered_books(request, users):
    for user in users:
        if (request.user.is_superuser or not user.showcaseDisabled) and len(user.offer_set.filter(active=True)) > 0:
            yield user

def filter_users_by_name_or_nick(user, nickname=None, real_name=None):
        if nickname:
            if user.username is not None and nickname.lower() in user.username.lower():
                yield user
        else:
            words = [x.lower() for x in real_name.split()]
            if len(words) == 2:
                if words[0].lower() in user.first_name.lower() and words[1] in user.last_name.lower():
                    yield user
                if words[1].lower() in user.first_name.lower() and words[0] in user.last_name.lower():
                    yield user

            else:
                for word in words:
                    if word in user.first_name.lower():
                        yield user
                    if word in user.last_name.lower():
                        yield user

def showcasesOverView(request):
    template_name = 'app_book/showcaseOverview.html'

    filteredUsers = []

    sellerNameFilteredUsers = []
    filteredUsers.extend(filter_users_with_offered_books(request, User.objects.all()))

    page = escape(request.GET.get('page'))
    order_by = escape(request.GET.get('order_by', 'date'))
    order_dir = escape(request.GET.get('order_dir', 'desc'))
    order_dir_is_desc = order_dir == 'desc'
    seller = escape(request.GET.get('seller', ''))

    if seller:
        for user in filteredUsers:
            if user.username is not None:
                sellerNameFilteredUsers.extend(filter_users_by_name_or_nick(user=user, nickname=seller))
            else:
                sellerNameFilteredUsers.extend(filter_users_by_name_or_nick(user=user, real_name=seller))
        filteredUsers = set(sellerNameFilteredUsers)
        filteredUsers = list(filteredUsers)

    for user in filteredUsers:
        user.books_count = len(user.offer_set.all())
        user.updated = (max(user.offer_set.all(), key=lambda offer: offer.updated)).updated

    if order_by == 'count':
        filteredUsers.sort(key=lambda user: user.books_count, reverse=order_dir_is_desc)
    elif order_by == 'name':
        filteredUsers.sort(key=lambda user: user.pseudonym_or_full_name().lower(), reverse=order_dir_is_desc)
    # TODO: user-rating
    # elif order_by == 'rating':
    #    filteredUsers.sort(key=lambda user: UserRating.calculate_stars_for_user(user.id), reverse=direction)
    else:
        # most recent update
        filteredUsers.sort(key=lambda user: user.updated, reverse=order_dir_is_desc)

    paginator = Paginator(filteredUsers, settings.MAX_ELEMENTS_PER_PAGE)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render_to_response(template_name, {
        "users": users,
        "order_by": order_by,
        "order_dir": order_dir,
        "request": request,
    }, RequestContext(request))


def newestBooks(request):
    template_name = 'app_book/newest_books.html'

    offers = Offer.objects.filter(active=True).order_by('-updated')

    return render_to_response(template_name, {
        "offers": offers,
    }, RequestContext(request))


# Call via AJAX
@login_required
def toggleDisabledState(request, user_id):
    if request.method == 'POST' and request.user.is_superuser:
        user = User.objects.filter(id=user_id).first()
        disabled = user.showcaseDisabled
        user.showcaseDisabled = not disabled
        user.save()
        return JsonResponse({'state': not disabled})
    return JsonResponse({'error': True})
