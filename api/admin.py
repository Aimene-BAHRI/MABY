from django.contrib import admin

from .models import Patient, Student, Doctor

# Register your models here.

admin.site.register(Patient)
admin.site.register(Student)
admin.site.register(Doctor)