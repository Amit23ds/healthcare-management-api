
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from accounts.models import User
from doctors.models import Doctor


class DoctorAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="doctoruser@example.com",
            name="Doctor User",
            password="TestPassword@123"
        )

        self.client.force_authenticate(user=self.user)

        self.doctor = Doctor.objects.create(
            name="Dr. Rajesh Kumar",
            specialization="Cardiology",
            email="rajesh@example.com",
            phone_number="9876543210"
        )

    def test_create_doctor(self):
        url = reverse("doctor-list-create")

        response = self.client.post(url, {
            "name": "Dr. Priya Sharma",
            "specialization": "Neurology",
            "email": "priya@example.com",
            "phone_number": "9876543211"
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Doctor.objects.count(), 2)

    def test_list_doctors(self):
        url = reverse("doctor-list-create")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_doctor(self):
        url = reverse(
            "doctor-detail",
            kwargs={"pk": self.doctor.id}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Dr. Rajesh Kumar")

    def test_delete_doctor(self):
        url = reverse(
            "doctor-detail",
            kwargs={"pk": self.doctor.id}
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Doctor.objects.filter(id=self.doctor.id).exists()
        )
