from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from patients.models import Patient

# Create your views here.


class PatientListView(LoginRequiredMixin, generic.ListView):
    model = Patient
    template_name = "reports/patients.html"
    context_object_name = "patient"

    def get_queryset(self, queryset=None):
        return Patient.objects.filter(is_active=True, user=self.request.user)
