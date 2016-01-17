# coding=utf-8
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime

from app_book.models import Book
from app_payment.models import Payment
from app_user.models import User
from .models import Notification
from django.contrib.auth.decorators import login_required

@login_required
def notificationPageView(request):
    '''
    Diese Methode zeigt alle vorhandenen Notifications an
    :param request: Der Request der erzeugt wurde
    :return: allNotifications: Alle Notifications
    '''
    notifications = Notification.objects.filter(receiver_user_id = request.current_user.id).order_by('-id')

    template_name = 'notifications.html'
    return render_to_response(template_name, {
        "notifications": notifications,
        "user": request.current_user,
    }, RequestContext(request))


# Call via AJAX
@login_required
def read_notification(request, id):
    notification = get_object_or_404(Notification, id=id)
    if request.method == 'POST':
        notification.read_at = datetime.now()
        notification.save()
        return JsonResponse({'read_at': notification.read_at})
    return JsonResponse({'error': True})

# Call via AJAX
@login_required
def notificationEmailToggle(request):
    if request.method == 'POST':
        user = request.current_user
        enabled = user.enabled_notifications_via_email
        user.enabled_notifications_via_email = not enabled
        user.save()
        return JsonResponse({'state': not enabled})
    return JsonResponse({'error': True})


@login_required
def notificationSendBookPageView(request, id):
    '''
    Diese Methode versendet eine Notification das das Buch versendet wurde
    :param request: Der Request der erzeugt wurde
    :id Id der der notification
    '''
    notification = get_object_or_404(Notification, id=id)
    if not notification.book:
        return HttpResponseRedirect(reverse('app_notification:notificationsPage'))
    buyer = get_object_or_404(User, id=notification.sender_user.id)
    seller = get_object_or_404(User, id=notification.receiver_user.id)
    book = get_object_or_404(Book, id=notification.book.id)
    payment = Payment.objects.filter(book=book).last()
    if request.user.pk is not seller.pk or book.is_in_active_payment_process() or payment.shipped:
        messages.add_message(request, messages.ERROR,
                         'Keine Berechtigung.')
        return HttpResponseRedirect(reverse('app_notification:notificationsPage'))

    Notification.send_book(id)
    messages.add_message(request, messages.SUCCESS,
                         'Versandstatus wurde erfolgreich geändert. Der Käufer wird benachrichtigt')
    return HttpResponseRedirect(reverse('app_notification:notificationsPage'))
