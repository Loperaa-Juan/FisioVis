from django.urls import path

from .views import PatientListView

urlpatterns = [
    path("patient_list/", PatientListView.as_view(), name="patient-reports")
]
