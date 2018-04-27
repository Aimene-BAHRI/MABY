"""medical URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import include, path
from inference.views import main
from api.resources import PatientResource, StudentResource, DoctorResource
from api.views import *

patient_resource = PatientResource()
student_resource = StudentResource()
doctor_resource = DoctorResource()

urlpatterns = [
    path('', view= main, name='main'),
    url(r'^Patient/new/$', view = patient_new, name='patient_new'),
    url(r'^Patient/(?P<pk>\d+)/edit/$', view = patient_edit, name='patient_edit'),
    url(r'^Student/new/$', view = student_new, name='student_new'),
    url(r'^Student/(?P<pk>\d+)/edit/$', view = student_edit, name='student_edit'),
    url(r'^Doctor/new/$', view = doctor_new, name='doctor_new   '),
    url(r'^Doctor/(?P<pk>\d+)/edit/$', view = doctor_edit, name='doctor_edit'),
    path('admin/', admin.site.urls),
    path('medical/', include('inference.urls')),

    url(r'^Patientapi/', include(patient_resource.urls)),
    url(r'^Studentapi/', include(student_resource.urls)),
    url(r'^Doctorapi/', include(doctor_resource.urls)),
]
