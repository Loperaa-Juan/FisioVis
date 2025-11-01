from django.urls import path
from .views import PatientListView
urlpatterns = [
    path('list/', PatientListView.as_view(), name='patient_list')
]
