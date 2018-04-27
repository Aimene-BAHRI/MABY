from django.db import models
 

# Create your models here.
class Patient(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    mail = models.CharField(max_length=200)
    local_adress = models.CharField(max_length=200)
    age = models.CharField(max_length=200)
    sexe = models.CharField(max_length=200)
    smoker = models.BooleanField(default=False)
    Chronical_disease = models.BooleanField(default=False)
    
    def __str__(self):
        return '%s %s' % (self.nom, self.prenom)

class Student(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    mail = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    speciality = models.CharField(max_length=200)
    
    def __str__(self):
        return '%s %s' % (self.nom, self.prenom)


class Doctor(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    mail = models.CharField(max_length=200)
    Work_adress = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    
    def __str__(self):
        return '%s %s' % (self.nom, self.prenom)


