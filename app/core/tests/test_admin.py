from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminTest(TestCase):
    def setUp(self):
        """
        function runs before every test
        """
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@email.com",
            password="admin")
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="user@email.com",
            password="123",
            name="Test"
        )

    def test_list_users(self):
        """Test that users are listed in user page"""
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_change_page(self):
        url = reverse('admin:core_user_change', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        url = reverse('admin:core_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
