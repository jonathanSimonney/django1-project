from elementaryCellularAutomata.forms import WolframForm
from django.views.generic.edit import FormView
import numpy
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.urls import reverse_lazy


class WolframAutomaton:
    X_DIM = 79
    Y_DIM = 40
    INIT_X_CELL = 39

    def __init__(self, rule_number):
        self.result_array = numpy.zeros((self.Y_DIM, self.X_DIM), dtype=int)
        self._fill_result_array(rule_number)

    def _get_cell_number_getter(self, rule_number):
        wolfram_rule = bin(rule_number)

        array_rule = [int(d) for d in str(wolfram_rule)[2:]]

        while len(array_rule) < 8:
            array_rule.insert(0, 0)

        corr_array = {
            "111": array_rule[0],
            "110": array_rule[1],
            "101": array_rule[2],
            "100": array_rule[3],
            "011": array_rule[4],
            "010": array_rule[5],
            "001": array_rule[6],
            "000": array_rule[7],
        }

        def get_cell_number(y, x):
            first_number = self.result_array[y - 1, x - 1] if x - 1 >= 0 else 0
            second_number = self.result_array[y - 1, x]
            third_number = self.result_array[y - 1, x + 1] if x + 1 <= self.X_DIM - 1 else 0
            array_key = str(first_number) + str(second_number) + str(third_number)
            return corr_array[array_key]

        return get_cell_number

    def _fill_result_array(self, rule_number):
        get_cell_number = self._get_cell_number_getter(rule_number)

        self.result_array[0, self.INIT_X_CELL] = 1

        for y in range(self.Y_DIM - 1):
            for x in range(self.X_DIM):
                self.result_array[y + 1, x] = get_cell_number(y + 1, x)

        return self.get_str_representation()

    def get_str_representation(self):
        buffer = []
        for y in range(self.Y_DIM):
            str_to_display = ""
            for x in range(self.X_DIM):
                if self.result_array[y, x] == 1:
                    str_to_display += "#"
                else:
                    str_to_display += "."
            buffer.append(str_to_display)
        final_str_to_display = '\n'.join(buffer)
        return final_str_to_display


# Create your views here.
def wolfram_display(request):
    rule_number = int(request.POST['rule_number'])
    if not 0 <= rule_number <= 256:
        raise ValidationError("parameter rule number should have a value between 0 and 256")

    string_representation = WolframAutomaton(rule_number).get_str_representation()
    print(string_representation)
    return render(request, 'elementaryCellularAutomata/wolfram_display.html', {
        'automata_string': string_representation,
    })


class WolframView(FormView):
    template_name = 'elementaryCellularAutomata/wolfram_form.html'
    form_class = WolframForm
    success_url = reverse_lazy('wolfram_automata_display')
