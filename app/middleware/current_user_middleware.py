from django.http import QueryDict

from app_user.models import User

class CurrentUserMiddleware(object):
    # return None: continue with other middlewares
    # return HttpResponse: response directly to client
    def process_request(self, request):
        if request.user is not None:
            request.user = User.objects.filter(id=request.user.id).first()
        return None
