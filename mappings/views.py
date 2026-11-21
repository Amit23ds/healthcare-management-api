
from django.shortcuts import get_object_or_404
from doctors.models import Doctor
from doctors.serializers import DoctorSerializer

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer


# Create a mapping and list ALL mappings
class MappingListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.all().select_related(
            "patient", "doctor"
        )


# GET: List mappings for a patient
# DELETE: Delete a mapping by its ID

class PatientMappingListDeleteView(generics.ListAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Doctor.objects.filter(
            patient_mappings__patient_id=self.kwargs["pk"],
            patient_mappings__patient__user=self.request.user
        ).distinct()

    def delete(self, request, *args, **kwargs):
        mapping = get_object_or_404(
            PatientDoctorMapping,
            pk=kwargs["pk"],
            patient__user=request.user
        )

        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
