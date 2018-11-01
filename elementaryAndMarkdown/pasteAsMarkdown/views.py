from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from pasteAsMarkdown.forms import PastebinForm
from django.http import HttpResponseRedirect
from pasteAsMarkdown.models import Pastebin
import uuid
from django.core.exceptions import ValidationError


# Create your views here.
class PastebinView(FormView):
    template_name = 'pasteAsMarkdown/pastebin_form.html'
    form_class = PastebinForm
    success_url = reverse_lazy('create_pastebin')


def create_pastebin(request):
    def pastebin_exists_with_this_path(path):
        try:
            Pastebin.objects.get(path=path)
        except Pastebin.DoesNotExist:
            return False
        return True

    def generate_random_path():
        while True:
            new_uuid = str(uuid.uuid4())[:40]
            if not pastebin_exists_with_this_path(new_uuid):
                return new_uuid

    post = request.POST.copy()
    user_path = post['path']
    given_path_changed = False
    if pastebin_exists_with_this_path(user_path):
        post['path'] = generate_random_path()
        given_path_changed = True
    f = PastebinForm(post)
    if f.is_valid():
        if f.instance.path == "":
            f.instance.path = generate_random_path()
        pastebin = f.save()
        # use given_path_changed to display a message if we changed the user path
        return HttpResponseRedirect(reverse('pasteAsMarkdown:show_result', args=(pastebin.path,)))
    form = PastebinForm
    return render(request, 'pasteAsMarkdown/pastebin_form.html', {
                        'form': form,
                        'error_message': f.errors,
                   })


def show_pastebin(request, pastebin_path):
    try:
        pastebin = Pastebin.objects.get(path=pastebin_path)
    except Pastebin.DoesNotExist:
        raise ValidationError("no pastebin found matching pastebin_path parameter")
    return render(request, 'pasteAsMarkdown/pastebin_display.html', {
        'markdown': pastebin.markdown_text,
    })
