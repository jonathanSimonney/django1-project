from django.forms import ModelForm
from pasteAsMarkdown.models import Pastebin


class PastebinForm(ModelForm):
    class Meta:
        model = Pastebin
        fields = ["markdown_text", "path"]
