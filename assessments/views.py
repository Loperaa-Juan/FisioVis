from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from patients.models import Patient

from .models import Assessment

# Create your views here.


@login_required
def assessment_list_view(request, id):
    patient = Patient.objects.get(id=id)
    assesments = Assessment.objects.get_queryset()
    return render(
        request,
        "assessments/list_assessments.html",
        {"patient": patient, "assessments": assesments},
    )


class AssessmentView(LoginRequiredMixin, generic.TemplateView):
    template_name = "assessments/assessment.html"
