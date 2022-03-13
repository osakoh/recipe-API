# custom user model
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

# constant variables
CREATE_USER_URL = reverse('user:create')  # /api/user/create/
TOKEN_URL = reverse('user:token')  # /api/user/token/
USER_UPDATE_PROFILE_URL = reverse('user:manage_user')  # /api/user/manage/


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

    def test_create_token_for_user(self):
        """ Test that a token is created for the user"""
        payload = {
            'email': 'a@a.com',
            'password': 'testtest',
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        # response should contain a key called token. i.e. res.data: {'token': 'someTokenHere'}
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ Test that token is not created if invalid credentials are given """
        create_user(email='a@a.com', password="testtest")  # correct credential of user
        # user supplied an incorrect password
        payload = {'email': 'a@a.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        # response shouldn't contain any token
        self.assertNotIn('token', res.data)
        # 404 status code since the password given was incorrect
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        # note: user must exist in DB before user can log in
        payload = {
            'email': 'a@a.com',
            'password': 'testtest',
        }
        res = self.client.post(TOKEN_URL, payload)

        # response shouldn't contain any token
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """ Test that email and password are required """
        payload = {
            'email': '',
            'password': '',
        }
        res = self.client.post(TOKEN_URL, payload)
        # response shouldn't contain any token
        self.assertNotIn('token', res.data)
        # 404 status code since the email & password given were incorrect / missing
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(USER_UPDATE_PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """ Test API endpoints which require authentication"""

    def setUp(self):
        self.user = create_user(
            email='abc@abc.com',
            password='testpass',
            name='Dave'
        )
        self.client = APIClient()
        # helper function for authenticating a user
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """ Test retrieving profile for logged in used"""
        res = self.client.get(USER_UPDATE_PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {'name': self.user.name, 'email': self.user.email})

    def test_post_manage_user_not_allowed(self):
        """ Test that POST is not allowed on the manage_user url """
        res = self.client.patch(USER_UPDATE_PROFILE_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'name': 'Billy', 'password': 'abcdef123'}

        res = self.client.patch(USER_UPDATE_PROFILE_URL, payload)
        # used between test when using the same user instance across multiple tests that updates the saved user state
        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
