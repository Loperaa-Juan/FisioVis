from django.urls import path

from .views import AssessmentView, assessment_list_view

urlpatterns = [
    path("list/<uuid:id>", assessment_list_view, name="list_assessments"),
    path("evaluate", AssessmentView.as_view(), name="evaluate"),
]
