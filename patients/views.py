from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from .forms import PatientForm
from .models import Patient


# Create your views here.
class PatientListView(LoginRequiredMixin, generic.ListView):
    model = Patient
    template_name = "patients/list_patient.html"
    context_object_name = "patient"

    def get_queryset(self, queryset=None):
        return Patient.objects.filter(is_active=True, user=self.request.user)


@login_required
def create_patient(request):
    if request.method == "GET":
        return render(request, "patients/create_patient.html", {"form": PatientForm})
    else:
        form = PatientForm(request.POST)
        new_patient = form.save(commit=False)
        new_patient.user = request.user
        new_patient.save()
        return redirect("patient_list")


@login_required
def patient_detail_view(request, id):
    patient = get_object_or_404(Patient, id=id)
    return render(request, "patients/patient_details.html", {"patient": patient})


@login_required
def update_patient_view(request, id):
    patient = get_object_or_404(Patient, id=id)

    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect("patient_list")
    else:
        form = PatientForm(instance=patient)

    return render(request, "patients/edit_patient.html", {"form": form})


def delete_patient_view(request, id):
    patient = get_object_or_404(Patient, id=id)

    if request.method == "POST":
        patient.delete()
        return redirect("patient_list")

    return render(request, "patients/delete_patient.html", {"patient": patient})
