from elementaryCellularAutomata.forms import WolframForm
from django.views.generic.edit import FormView


# Create your views here.
def wolfram_display(request, question_id):
    # TODO
    print("salut")


class WolframView(FormView):
    template_name = 'elementaryCellularAutomata/wolfram_form.html'
    form_class = WolframForm
    success_url = '/show/'
