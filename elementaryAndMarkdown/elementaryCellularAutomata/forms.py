from django import forms


class WolframForm(forms.Form):
    rule_number = forms.IntegerField(min_value=0, max_value=256)
