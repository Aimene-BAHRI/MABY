from django.shortcuts import render
from .forms import *

# Create your views here.
def patient_new(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.author = request.user
            patient.save() 
            return redirect('patient_detail', pk=patient.pk) #TODO add detail option µDone
    else:
        form = PatientForm()

    return render(request, 'edit/patient_edit.html', {'form': form})
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        form = PatientForm(request.Patient, instance=patient)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.author = request.user
            patient.save()
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'edit/patient_edit.html', {'form': form})

def student_new(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.author = request.user
            student.save()
            return redirect('student_detail', pk=student.pk) #TODO add detail option µDone
    else:
        form = StudentForm()

    return render(request, 'edit/student_edit.html', {'form': form})
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.Student, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.author = request.user
            student.save()
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    return render(request, 'edit/student_edit.html', {'form': form})

def doctor_new(request):
    if request.method == "POST":
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.author = request.user
            doctor.save()
            return redirect('doctor_detail', pk=doctor.pk) #TODO add detail option µDone
    else:
        form = DoctorForm()
    
    return render(request, 'edit/doctor_edit.html', {'form': form})
def doctor_edit(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == "POST":
        form = DoctorForm(request.Doctor, instance=doctor)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.author = request.user
            doctor.save()
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'edit/doctpor_edit.html', {'form': form})