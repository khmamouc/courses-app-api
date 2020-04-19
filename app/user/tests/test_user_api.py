from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """Helper function to create new user"""
    return get_user_model().objects.create_user(**params)


class UserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        """Test creating using with a valid payload is successful"""
        payload = {
            'email': 'test@email.com',
            'password': 'pwd123',
            'name': 'name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(
            user.check_password(payload['password'])
        )
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {'email': 'test@email.com',
                   'password': 'pwd123'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_pwd(self):
        """Test that password must be more than 5 characters"""
        payload = {'email': 'test@email.com',
                   'password': 'pw',
                   'name': 'test name'
                   }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_valid_user(self):
        """ Test token creation for a valid user"""
        payload = {
            'email': 'test@email.com',
            'password': 'pwd123'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_invalid_user(self):
        """ Test that token is not created for user with wrong credentials"""
        create_user(
            email="test@email.com",
            password="pwd123"
        )
        payload = {
            "email": "test@email.com",
            "password": "wrongpass"
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """test that a token is  not created for a non existing user"""
        payload = {
            "email": "test@email.com",
            "password": "wrongpass"
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_field(self):
        payload = {"email": "test@email.com", "password": ""}

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_unauthorized(self):
        """ Test that auth is required """

        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """ Test API request requiring authentication """

    def setUp(self):
        self.user = create_user(
            email='test@email.com',
            password="pw123",
            name='test name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_success(self):
        """ Test retrieving user successful """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email

        })

    def test_not_allowed(self):
        """ Test that post is not allowed it the me url """
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_404_METHOD_NOT_ALLOWED)

    def test_update_user(self):
        """ Test updating a profile of authenticating user """
        payload = {
            'email': 'test@email.com',
            'password': 'pwd123',
            'name': 'test name',
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
