# -*- coding: utf-8 -*-

from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import StaticPage
from .forms import StaticPageForm

from app_payment.models import SellerRating
from app_user.models import User
from app_book.models import Offer
from app_book.views import filter_users_with_offered_books

import calendar, time, datetime


def start_page_view(request, elems=5):
    template_name = 'app/start.html'

    filtered_users = []
    filtered_users.extend(filter_users_with_offered_books(request, User.objects.all()))

    for user in filtered_users:
        user.books_count = len(user.offer_set.all())
        user.updated = (max(user.offer_set.all(), key=lambda offer: offer.updated)).updated

    filtered_users.sort(key=lambda user: user.updated, reverse=True)
    filtered_users = filtered_users[:elems]

    filtered_offers = []
    filtered_offers.extend(Offer.objects.filter(active=True))
    filtered_offers.sort(key=lambda offer: offer.updated, reverse=True)
    filtered_offers = filtered_offers[:elems]

    citations = [
        'Die Erfindung des Buchdruckes ist das größte Ereignis der Weltgeschichte.',
        'Erst durch Lesen lernt man, wieviel man ungelesen lassen kann.',
        'Um das Gute lesen zu können, ist es Bedingung, dass man das Schlechte nicht lese.',
        'Eine schädliche Folge des allzu vielen Lesens ist, dass sich die Bedeutung der Wörter abnutzt.',
        'Es gibt keinen schlimmeren Räuber als ein schlechtes Buch.',
        'Mitunter las ich ein Buch mit Vergnügen...',
        'Bücher lesen heißt wandern gehen in ferne Welten, aus den Stuben, über die Sterne.',
        'Hast du drei Tage kein Buch gelesen, werden deine Worte seicht.',
        'Der wahre Leser muss der erweiterte Autor sein.',
        'Beim Lesen lässt sich vortrefflich denken.',
        'Das Lesen lässt die Vergangenheit in Gegenwart wandern.',
        'Wer zu lesen versteht, besitzt den Schlüssel zu großen Taten, zu unerträumten Möglichkeiten.',
        'Auch das schlechteste Buch hat seine gute Seite: die letzte!',
        'Fernsehen bildet. Immer, wenn der Fernseher an ist, gehe ich in ein anderes Zimmer und lese.',
        'Wer in der Zukunft lesen will, muss in der Vergangenheit blättern.',
        'Bücher sind Schiffe, welche die weiten Meere der Zeit durcheilen.',
        'Schon oft hat das Lesen eines Buches jemandes Zukunft beeinflußt.',
    ]
    current_epoch = calendar.timegm(time.gmtime())
    citation = citations[current_epoch % len(citations)]

    return render_to_response(template_name, {
        "title": 'SDF',
        "citation": citation,
        "users": filtered_users,
        "offers": filtered_offers,
    }, RequestContext(request))


def raise_exception(request):
    raise Exception("Exception for testing via GET /raise")

def staticPageView(request, name):
    page = StaticPage.objects.filter(name=name).first()

    if page == None or (request.method == 'POST' and not request.user.is_superuser):
        messages.add_message(request, messages.ERROR, 'Ungültiger Vorgang!')
        return HttpResponseRedirect(reverse('app:startPage'))

    form = staticPageEdit(request,page)

    return render_to_response("app/staticPage.html", {"page":page, "form":form}, RequestContext(request))

@login_required
def staticPageEdit(request, page):
    form = StaticPageForm(request.POST, instance=page)

    if request.method == 'POST':
        form = StaticPageForm(request.POST, instance=page)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Statischer Inhalt wurde geändert!')
        else:
            messages.add_message(request, messages.ERROR, 'Statischer Inhalt konnte nicht geändert werden!')
    else:
        form = StaticPageForm(instance=page)

    return form
