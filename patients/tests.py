
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from accounts.models import User
from patients.models import Patient


class PatientAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="patientuser@example.com",
            name="Patient User",
            password="TestPassword@123"
        )

        self.other_user = User.objects.create_user(
            email="otheruser@example.com",
            name="Other User",
            password="TestPassword@123"
        )

        self.client.force_authenticate(user=self.user)

        self.patient = Patient.objects.create(
            user=self.user,
            name="Rahul Sharma",
            age=28,
            gender="Male",
            address="Bengaluru",
            phone_number="9876543210"
        )

    def test_create_patient(self):
        url = reverse("patient-list-create")

        response = self.client.post(url, {
            "name": "Amit Sharma",
            "age": 25,
            "gender": "Male",
            "address": "Bengaluru",
            "phone_number": "9876543211"
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 2)

    def test_list_only_own_patients(self):
        Patient.objects.create(
            user=self.other_user,
            name="Other Patient",
            age=30,
            gender="Female",
            address="Delhi",
            phone_number="9876543212"
        )

        url = reverse("patient-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_cannot_access_other_users_patient(self):
        other_patient = Patient.objects.create(
            user=self.other_user,
            name="Other Patient",
            age=30,
            gender="Female",
            address="Delhi",
            phone_number="9876543212"
        )

        url = reverse(
            "patient-detail",
            kwargs={"pk": other_patient.id}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_own_patient(self):
        url = reverse(
            "patient-detail",
            kwargs={"pk": self.patient.id}
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Patient.objects.filter(id=self.patient.id).exists()
        )
