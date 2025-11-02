from django.views import generic

from .models import Assessment

# Create your views here.


class AssessmentsListView(generic.ListView):
    model = Assessment
    template_name = "assessments/list_assessments.html"
    context_object_name = "assessments"
    template_name = "assessments/list_assessments.html"
    context_object_name = "assessments"
