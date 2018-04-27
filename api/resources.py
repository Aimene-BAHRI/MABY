from tastypie.resources import ModelResource
from api.models import *

class PatientResource(ModelResource):
    class Meta:
        queryset = Patient.objects.all()
        resource_name = 'patient'

class StudentResource(ModelResource):
    class Meta:
        queryset = Student.objects.all()
        resource_name = 'student'

class DoctorResource(ModelResource):
    class Meta:
        queryset = Doctor.objects.all()
        resource_name = 'doctor'

