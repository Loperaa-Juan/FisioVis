from django.urls import path

from .views import PatientListView, create_report

urlpatterns = [
    path("patient_list/", PatientListView.as_view(), name="patient-reports"),
    path("create_report/<uuid:id>", create_report, name="create_report"),
]
