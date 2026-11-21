
from django.urls import path

from .views import (
    MappingListCreateView,
    PatientMappingListDeleteView,
)

urlpatterns = [
    path(
        "",
        MappingListCreateView.as_view(),
        name="mapping-list-create"
    ),
    path(
        "<int:pk>/",
        PatientMappingListDeleteView.as_view(),
        name="mapping-patient"
    ),
]
