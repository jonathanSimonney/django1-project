from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from pasteAsMarkdown.forms import PastebinForm
from django.http import HttpResponseRedirect
from pasteAsMarkdown.models import Pastebin
import uuid


# Create your views here.
class PastebinView(FormView):
    template_name = 'pasteAsMarkdown/pastebin_form.html'
    form_class = PastebinForm
    success_url = reverse_lazy('create_pastebin')


def create_pastebin(request):
    def generate_random_path():
        while True:
            new_uuid = uuid.uuid4()
            try:
                Pastebin.objects.get(path=new_uuid)
            except Pastebin.DoesNotExist:
                return new_uuid

    f = PastebinForm(request.POST)
    if f.is_valid():
        if f.instance.path is None:
            f.instance.path = generate_random_path()
        pastebin = f.save()
        return HttpResponseRedirect(reverse('pasteAsMarkdown:show_result', args=(pastebin.path,)))
    form = PastebinForm
    return render(request, 'pasteAsMarkdown/pastebin_form.html', {
                        'form': form,
                        'error_message': 'you submitted invalid data',
                   })


def show_pastebin(request, pastebin_path):
    ...
