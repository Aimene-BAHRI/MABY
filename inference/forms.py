from django import forms


class InferenceForm(forms.Form):
    age = forms.IntegerField()
    glycemie = forms.FloatField()
    conscient = forms.BooleanField(required=False)
