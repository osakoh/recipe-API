from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "a@a.com"
        password = "testpass"
        user = get_user_model().objects.create_user(email=email, password=password)

        # expected email(email), actual email(user.email)
        self.assertEqual(user.email, email)
        # expected password(check_password(password)), actual password(user.password)
        # check_password returns true / false
        self.assertTrue(user.check_password(password))
