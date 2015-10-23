from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.forms.models import modelformset_factory
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

from .forms import NewBookForm
from .models import Book

class StartPageView(TemplateView):
    template_name = 'app/start.html'

    def get_context_data(self, **kwargs):
        context = super(StartPageView, self).get_context_data(**kwargs)
        return context


def archivesPageView(request):
    template_name = 'app/archives.html'
    collapsed = False

    newBookFormSet = modelformset_factory(Book, NewBookForm)
    if request.method == 'POST':
        try:
            formset = newBookFormSet(request.POST)
            NewBookForm.validateAndSaveNewBook(formset)
            formset = newBookFormSet(queryset=Book.objects.filter(name__startswith='O'))
            collapsed = True
            messages.add_message(request, messages.SUCCESS, 'Das Buch wurde erfolgreich angelegt!')
        except ValidationError as e:
            messages.add_message(request, messages.ERROR, 'Das Buch konnte leider nicht gespeichert werden!')
    else:
        formset = newBookFormSet(queryset=Book.objects.filter(name__startswith='O'))
        collapsed = True

    allSavedCustomerBooks=Book.objects.all();



    return render_to_response(template_name, {
        "formset": formset,
        "collapsed": collapsed,
        "allSavedCustomerBooks": allSavedCustomerBooks,
    },  RequestContext(request))



