# coding=utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime

from .models import Notification
from django.contrib.auth.decorators import login_required

@login_required
def notificationPageView(request):
    '''
    Diese Methode zeigt alle vorhandenen Notifications an
    :param request: Der Request der erzeugt wurde
    :return: allNotifications: Alle Notifications
    '''
    notifications = Notification.objects.filter(receiver_user_id = request.user.id).order_by('-id')

    template_name = 'notifications.html'
    return render_to_response(template_name, {
        "notifications": notifications,
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


@login_required
def notificationSendBookPageView(request, id):
    '''
    Diese Methode versendet eine Notification das das Buch versendet wurde
    :param request: Der Request der erzeugt wurde
    :id Id der der notification
    '''
    Notification.send_book(id);

    messages.add_message(request, messages.SUCCESS,
                         'Versandstatus wurde erfolgreich geändert. Der Käufer wird benachrichtigt')
    return HttpResponseRedirect(reverse('app_notification:notificationsPage'))
