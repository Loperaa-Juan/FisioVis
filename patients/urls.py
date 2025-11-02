from django.urls import path

from .views import PatientListView, create_patient, patient_detail_view, update_patient_view

urlpatterns = [
    path("list/", PatientListView.as_view(), name="patient_list"),
    path("create/", create_patient, name="create_patient"),
    path("details/<uuid:id>", patient_detail_view, name="detail_view"),
    path('update/<uuid:id>', update_patient_view, name='update_patient')
]
