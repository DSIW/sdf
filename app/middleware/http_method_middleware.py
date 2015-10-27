from django.http import QueryDict

class HttpMethodMiddleware(object):
    # return None: continue with other middlewares
    # return HttpResponse: response directly to client
    def process_request(self, request):
        method = request.POST.get('_method', request.method)
        if method.lower() == 'put':
            request.method = 'PUT'
            request.META['REQUEST_METHOD'] = 'PUT'
            request.PUT = QueryDict(request.body)
            request.META['HTTP_X_CSRFTOKEN'] = QueryDict(request.body).get('csrfmiddlewaretoken')
        if method.lower() == 'delete':
            request.method = 'DELETE'
            request.META['REQUEST_METHOD'] = 'DELETE'
            request.DELETE = QueryDict(request.body)
            request.META['HTTP_X_CSRFTOKEN'] = QueryDict(request.body).get('csrfmiddlewaretoken')
        return None
