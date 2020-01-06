from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            email='admin@recipes.com',
            password='admin'
        )
        self.client.force_login(self.admin)
        self.user = get_user_model().objects.create_user(
            email='example@gmail.com',
            password='password',
            name='User full name'
        )

    def test_users_listed(self):
        """Test users that are in the list on user page"""
        url = reverse('admin:core_user_changelist')                 # Generate url for user page
        response = self.client.get(url)
        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_change_page(self):
        """Test user editing page is ok"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        result = self.client.get(url)

        self.assertEqual(result.status_code, 200)       # Http response is ok 200

    def test_user_page_render(self):
        """Test user page works"""
        url = reverse('adnin: core_user_add')
        result = self.client.get(url)
        self.assertEqual(result.status_code, 200)