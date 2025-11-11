from django.urls import path

from .views import assessment_view, evaluate, save_assessment

urlpatterns = [
    path("evaluate/<uuid:id>", assessment_view, name="evaluate"),
    path("eval", evaluate, name="evaluate_moves"),
    path("save", save_assessment, name="save-assessment"),
]
