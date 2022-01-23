from django.contrib.auth import get_user_model
from django.test import TestCase


def sample_user(email="a@a.com", password="test123"):
    """returns a sample user with an email and password"""
    return get_user_model().objects.create_user(email, password)


def sample_super_user(email="a@a.com", password="test123"):
    """returns a sample user with an email and password"""
    return get_user_model().objects.create_superuser(email, password)


class ModelTests(TestCase):
    """test the models"""

    def test_create_user_with_email_successful(self):
        """test creating a new user with an email is successful"""
        email = "a@a.com"
        password = "test123"
        # user = get_user_model().objects.create_user(email=email, password=password)
        user = sample_user()

        # expected email(email), actual email(user.email)
        self.assertEqual(user.email, email)
        # expected password(check_password(password)), actual password(user.password)
        # check_password: returns true if password is correct otherwise False
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """test the normalisation of new user email"""
        email = "a@A.COM"
        # user = get_user_model().objects.create_user(email, "test123")
        user = sample_user()

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """test if a ValueError is raised if no email is supplied by the user"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test123")

    def test_create_new_superuser(self):
        """test creation of superuser"""
        # email = "a@A.COM"
        # password = "test123"
        # user = get_user_model().objects.create_superuser(email, password)
        user = sample_super_user()

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


print(f"\n**********************{ModelTests().__class__.__name__} now running ***********************\n")

# docker-compose run app sh -c "python manage.py test"
