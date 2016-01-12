# -*- coding: utf-8 -*-

from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from .models import FAQ
from .forms import FAQForm
from app_user.models import User
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect

from django.core.urlresolvers import reverse

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
        user.books_count = len(user.offer_set.exclude(active = False))
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

def faq_list(request):
    return render_to_response('app/faq_list.html',{'faqs':FAQ.objects.order_by('position')},RequestContext(request))

def faq(request,id):
    entry = get_object_or_404(FAQ,id=id)
    return render_to_response('app/faq.html',{'faq':entry},RequestContext(request))


@login_required
@staff_member_required
def faq_create(request):
    if request.method == 'POST':
        form = FAQForm(data=request.POST)
        if form.is_valid():
            form.save(commit= False)
            form.instance.author = User.objects.filter(pk=request.user.id).first()
            form.save()
            messages.add_message(request, messages.SUCCESS, 'FAQ-Eintrag wurde erfolgreich erstellt!')
            return HttpResponseRedirect(reverse('app:faq_list'))
        else :
            messages.add_message(request, messages.ERROR, 'Der Eintrag konnte leider nicht gespeichert werden. Bitte prüfen Sie ihre Eingabe!')
            return render_to_response('app/faq_form.html', {'form': form, 'author': request.user,'action':'app:faq_create'}, RequestContext(request))
    else:
        form = FAQForm()
        return render_to_response('app/faq_form.html', {'form': form, 'author': request.user, 'action':'app:faq_create'}, RequestContext(request))

@login_required
@staff_member_required
def faq_edit(request,id):
    entry = get_object_or_404(FAQ,id=id)
    if request.method == 'POST':
        form = FAQForm(data=request.POST, instance=entry)
        if form.is_valid():
            form.save(commit= False)
            form.instance.author = User.objects.filter(pk=request.user.id).first()
            form.save()
            messages.add_message(request, messages.SUCCESS, 'FAQ-Eintrag wurde erfolgreich aktualisiert!')
            return HttpResponseRedirect(reverse('app:faq_list'))
        else :
            messages.add_message(request, messages.ERROR, 'Der Eintrag konnte leider nicht gespeichert werden. Bitte prüfen Sie ihre eingabe!')
            return render_to_response('app/faq_form.html', {'form': form, 'author': request.user, 'action': 'app:faq_edit','id':entry.id}, RequestContext(request))
    else:
        form = FAQForm(instance=entry)
        return render_to_response('app/faq_form.html', {'form': form, 'author': request.user, 'action': 'app:faq_edit', 'id':entry.id}, RequestContext(request))



@login_required
@staff_member_required
def faq_delete(request,id):
    if request.method == 'DELETE':
        entry = get_object_or_404(FAQ,id=id)
        if entry is not None:
            entry.delete()
            messages.add_message(request, messages.SUCCESS, 'Der FAQ-Eintrag ist erfolgreich gelöscht worden.')
            return HttpResponseRedirect(reverse('app:faq_list'))
        else:
            messages.add_message(request, messages.ERROR, 'Der FAQ-Eintrag konnte nicht gelöscht werden, da er nicht gefunden wurde.')
            return HttpResponseRedirect(reverse('app:faq_list'))
    else:
        raise BaseException("Use http method DELETE for deleting a faq-entry.")

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
