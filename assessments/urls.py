from django.urls import path

from .views import AssessmentsListView

urlpatterns = [
    path('list', AssessmentsListView.as_view(), name='list_assessments')
]
