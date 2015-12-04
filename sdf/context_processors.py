from django.conf import settings

def debug(context):
    #Can be used to check for debug mode inside templates
    return {'DEBUG': settings.DEBUG}