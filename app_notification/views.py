# coding=utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
# Create your views here.

from .models import Notification

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