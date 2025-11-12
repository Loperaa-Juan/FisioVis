import uuid

from django.db import models
from patients.models import Patient

# Create your models here.


class Assessment(models.Model):
    MOVEMENT_TYPES = (
        ("flexion", "Flexión"),
        ("extension", "Extensión"),
        ("flexo-extension", "Flexo-Extensión"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(max_length=100, null=True, verbose_name="nombre")
    description = models.TextField(
        max_length=500, null=True, verbose_name="descripción"
    )
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)

    def __str__(self):
        return self.name


class PatientAssessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    angle = models.IntegerField()
    photo = models.ImageField(null=True, blank=True, verbose_name="foto")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.id)} - {self.patient} - {self.assessment} -{self.date} - {self.angle}"
