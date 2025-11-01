import uuid

from django.db import models

from patients.models import Patient


# Create your models here.
class MotionAssessment(models.Model):
    MOVEMENT_TYPES = (
        ("flexion", "Flexión"),
        ("extension", "Extensión"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    angle = models.FloatField()
    ai_observation = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
