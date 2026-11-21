
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from accounts.models import User
from patients.models import Patient
from doctors.models import Doctor
from mappings.models import PatientDoctorMapping


class PatientDoctorMappingTests(APITestCase):

    def setUp(self):
        # Create two users
        self.user = User.objects.create_user(
            email="user1@example.com",
            name="User One",
            password="TestPassword@123"
        )

        self.other_user = User.objects.create_user(
            email="user2@example.com",
            name="User Two",
            password="TestPassword@123"
        )

        # Create a patient belonging to the first user
        self.patient = Patient.objects.create(
            user=self.user,
            name="Rahul Sharma",
            age=28,
            gender="Male",
            address="Bengaluru",
            phone_number="9876543210"
        )

        # Create a doctor
        self.doctor = Doctor.objects.create(
            name="Dr. Rajesh Kumar",
            specialization="Cardiology",
            email="doctor@example.com",
            phone_number="9876543211"
        )

        self.client.force_authenticate(user=self.user)

    def test_create_mapping(self):
        url = reverse("mapping-list-create")

        response = self.client.post(url, {
            "patient": self.patient.id,
            "doctor": self.doctor.id
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PatientDoctorMapping.objects.count(), 1)

    def test_duplicate_mapping_not_allowed(self):
        PatientDoctorMapping.objects.create(
            patient=self.patient,
            doctor=self.doctor
        )

        url = reverse("mapping-list-create")

        response = self.client.post(url, {
            "patient": self.patient.id,
            "doctor": self.doctor.id
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_map_another_users_patient(self):
        other_patient = Patient.objects.create(
            user=self.other_user,
            name="Other Patient",
            age=30,
            gender="Female",
            address="Bengaluru",
            phone_number="9876543212"
        )

        url = reverse("mapping-list-create")

        response = self.client.post(url, {
            "patient": other_patient.id,
            "doctor": self.doctor.id
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_mapping(self):
        mapping = PatientDoctorMapping.objects.create(
            patient=self.patient,
            doctor=self.doctor
        )

        url = reverse(
            "mapping-patient",
            kwargs={"pk": mapping.id}
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PatientDoctorMapping.objects.count(), 0)

    
    def test_list_mappings_for_patient(self):
        PatientDoctorMapping.objects.create(
            patient=self.patient,
            doctor=self.doctor
        )

        url = reverse(
            "mapping-patient",
            kwargs={"pk": self.patient.id}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        self.assertEqual(
            response.data[0]["name"],
            "Dr. Rajesh Kumar"
        )

        self.assertIn("specialization", response.data[0])
        self.assertNotIn("patient", response.data[0])
        self.assertNotIn("assigned_at", response.data[0])

