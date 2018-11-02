from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from pasteAsMarkdown.forms import PastebinForm
from django.http import HttpResponseRedirect
from pasteAsMarkdown.models import Pastebin
import uuid
import urllib.parse
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods


# Create your views here.
class PastebinView(FormView):
    http_method_names = ['get']
    template_name = 'pasteAsMarkdown/pastebin_form.html'
    form_class = PastebinForm
    success_url = reverse_lazy('create_pastebin')


@require_http_methods(["POST"])
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
    newer_path = None
    if pastebin_exists_with_this_path(user_path):
        post['path'] = generate_random_path()
        given_path_changed = True
    f = PastebinForm(post)
    if f.is_valid():
        if f.instance.path == "":
            f.instance.path = generate_random_path()
        pastebin = f.save()
        # use given_path_changed to display a message if we changed the user path
        return HttpResponseRedirect(reverse('pasteAsMarkdown:show_result', args=(pastebin.path,))
                                    + "?" + urllib.parse.urlencode({
                                        'pathChanged': given_path_changed,
                                        'olderPath': user_path,
                                        'newerPath': f.instance.path,
                                    }))
    form = PastebinForm
    return render(request, 'pasteAsMarkdown/pastebin_form.html', {
                        'form': form,
                        'error_message': f.errors,
                   })


@require_http_methods(["GET"])
def show_pastebin(request, pastebin_path):
    try:
        pastebin = Pastebin.objects.get(path=pastebin_path)
    except Pastebin.DoesNotExist:
        raise ValidationError("no pastebin found matching pastebin_path parameter")
    get = request.GET

    path_changed = get['pathChanged'] == "True" if 'pathChanged' in get else False
    older_path = get['olderPath'] if 'olderPath' in get else None
    newer_path = get['newerPath'] if 'newerPath' in get else None

    return render(request, 'pasteAsMarkdown/pastebin_display.html', {
        'markdown': pastebin.markdown_text,
        'display_path_changed': path_changed,
        'older_path': older_path,
        'newer_path': newer_path,
    })
