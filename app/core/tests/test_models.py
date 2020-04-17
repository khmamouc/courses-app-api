from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """ Test that creating a user with email is successful"""
        email = "test@email.com"
        password = "testpassword123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        # The password is encrypted
        self.assertTrue(user.check_password(password))

    def test_normalized_email(self):
        """ test that email is lower"""
        email = "test@EMAIL.com"
        password = "test123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email.lower())

    def test_invalid_email(self):
        """test that None value raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password="123"
            )

    def test_superuser(self):
        user = get_user_model().objects.create_superuser(
            email="superuser@email.com",
            password="123"
        )
        print(user)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
