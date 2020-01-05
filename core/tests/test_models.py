from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating new user with ok email"""
        email = 'example@gmail.com'
        password = 'password'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email of new user is normalized"""
        email = 'example@gmail.de'
        user = get_user_model().objects.create_user(email, 'password')

        self.assertEqual(user.email, email.lower())

    def test_new_user_email_invalid(self):
        """Test invalid email value error of user"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'PASSWORD')

    def test_create_superuser(self):
        """Test for creating superuser"""
        user = get_user_model().objects.create_user(
            'example@gmail.com',
            'password'
        )
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.is_staff)
