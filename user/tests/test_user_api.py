from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test API for public users """
    def setUp(self):
        self.client = APIClient()

    def test_validated_created_user_success(self):
        """Test creating user is ok"""
        payload = {
            'name': 'test',
            'password': 'password',
            'email': 'test@test.com'
        }

        result = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**result.data)  # Refer to payload
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', result.data)

    def test_user_exits(self):
        payload = {'email': 'test@test.com', 'password': 'password'}
        create_user(**payload)

        result = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password shoul be more than 8 chars"""
        payload = {'email' : 'test@test.com', 'password':'password'}
        result = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)