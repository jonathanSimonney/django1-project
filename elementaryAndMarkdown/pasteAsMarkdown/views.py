from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from pasteAsMarkdown.forms import PastebinForm


# Create your views here.
class PastebinView(FormView):
    template_name = 'pasteAsMarkdown/pastebin_form.html'
    form_class = PastebinForm
    success_url = reverse_lazy('create_pastebin')

def create_pastebin(request):
    ...
