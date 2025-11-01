from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Patients(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.TextField(max_length=100, verbose_name="Nombre Completo")
    age = models.IntegerField()
    work = models.TextField(max_length=200, verbose_name="Trabajo")
    medical_history = models.TextField(max_length=500, verbose_name="Antecedentes")
    surgeries = models.TextField(max_length=500, blank=True, null=True,verbose_name="Cirugías")
    pathologies = models.TextField(max_length=500, blank=True, null=True, verbose_name="Patologías")
    medications = models.TextField(max_length=500, blank=True, null=True, verbose_name="Medicamentos")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.full_name} was created!'