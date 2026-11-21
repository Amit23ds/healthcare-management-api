
from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.models import Patient
from doctors.models import Doctor


class PatientDoctorMappingSerializer(serializers.ModelSerializer):

    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all()
    )

    doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all()
    )

    class Meta:
        model = PatientDoctorMapping
        fields = ["id", "patient", "doctor", "assigned_at"]
        read_only_fields = ["id", "assigned_at"]

    def validate_patient(self, patient):
        request = self.context.get("request")

        if request and patient.user != request.user:
            raise serializers.ValidationError(
                "You can only assign doctors to your own patients."
            )

        return patient

    def validate(self, attrs):
        patient = attrs.get("patient")
        doctor = attrs.get("doctor")

        if patient and doctor:
            existing = PatientDoctorMapping.objects.filter(
                patient=patient,
                doctor=doctor
            )

            if self.instance:
                existing = existing.exclude(pk=self.instance.pk)

            if existing.exists():
                raise serializers.ValidationError(
                    "This doctor is already assigned to this patient."
                )

        return attrs
