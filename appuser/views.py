from django.shortcuts import render

from django.views.generic.edit import UpdateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .models import User

from .forms import RegistrationForm
# Create your views here.

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Sie haben sich erfolgreich registriert.')
            return HttpResponseRedirect(reverse('startPage'))
    else:
        form = RegistrationForm()
    return render_to_response('app/register.html', {'form': form}, RequestContext(request))



class UserUpdate(UpdateView):
    model = User
    fields = ['username','first_name', 'last_name', 'email', 'paypal']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('startPage')