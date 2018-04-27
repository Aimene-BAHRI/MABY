from django.shortcuts import render
from pyknowlib import orc

from .forms import InferenceForm


def index(request):
    if request.method == 'POST':
        form = InferenceForm(request.POST)

        if form.is_valid():
            age = form.cleaned_data['age']
            glycemie = form.cleaned_data['glycemie']
            conscient = form.cleaned_data['conscient']

            chaine = orc.execution(age, glycemie, conscient)

            return render(request, '../templates/medical/index.html', {'req': False,'form': form,'chaine' : chaine})

    else:
        form = InferenceForm()

    return render(request, '../templates/medical/index.html', {'req': True,'form': form})
                                                               

def main(request):
    return render(request, '../templates/medical/main.html')