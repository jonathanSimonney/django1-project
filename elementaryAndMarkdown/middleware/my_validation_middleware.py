from django.http import Http404, HttpResponse
from django.core.exceptions import ValidationError


class CustomValidationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, ValidationError):
            # implement your custom logic. You can send
            # http response with any template or message
            # here. unicode(exception) will give the custom
            # error message that was passed.
            msg = str(exception)
            return HttpResponse(msg, status=400)
