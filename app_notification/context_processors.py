from .models import Notification

def unread_notification_exist(request):
    unread_notifications = Notification.objects.filter(receiver_user_id = request.user.id, read_at__isnull=True)
    unread = unread_notifications.count() > 0
    return {'unread_notification_exist': unread}
