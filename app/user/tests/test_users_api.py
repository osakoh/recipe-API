from django.test import TestCase
# custom user model
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# constant variables
CREATE_USER_URL = reverse('user:create')  # /api/user/create/


def create_user(**params):
    """ Helper function to create users for test """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """ Test the users API that's public or un-authenticated """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """ Test successful creation of user with valid payload/data """
        payload = {
            'email': 'a@a.com',
            'password': 'test123',
            'name': 'Mark Bin'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        # test status code, 201
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # unpack key arguments i.e: **res.data: {'email': 'a@a.com', 'name': 'Mark Bin'}
        user = get_user_model().objects.get(**res.data)
        # check that the password is contained in the payload
        self.assertTrue(user.check_password(payload['password']))
        # check that the password is not returned as part of the response for security purposes
        self.assertNotIn('password', res.data)

    def test_duplicate_user(self):
        """ Test creating a duplicated/existing user """
        payload = {
            'email': 'a@a.com',
            'password': 'test123',
            'name': 'Mark Bin'
        }
        # using the helper function for creating a new user
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        # new user should not be created as the status code returned 400
        # res.data['email']: [ErrorDetail(string='A user is already registered with this email address', code='unique')]
        # res.data['email'][0]: A user is already registered with this email address
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'a@a.com',
            'password': 'tes',
            'name': 'Mark Bin'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        # status_code of 400 because user password is less than 5 characters
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # test user was not created i.e
        # new user should not be created as the status code returned 400
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)
