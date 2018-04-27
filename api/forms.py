from django import forms

from .models import *

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('nom', 'prenom', 'mail', 'local_adress', 'age', 'sexe')

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('nom', 'prenom', 'mail', 'university', 'speciality')

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('nom', 'prenom', 'mail', 'Work_adress', 'phone')

