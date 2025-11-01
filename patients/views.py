from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .models import Patient


# Create your views here.
class PatientListView(LoginRequiredMixin, generic.ListView):
    model = Patient
    template_name = "patients/list_patient.html"
    context_object_name = "patient"

    def get_object(self, queryset=None):
        return Patient.objects.filter(is_active=True, user=self.request.user).first()
        return Patient.objects.filter(is_active=True, user=self.request.user).first()
