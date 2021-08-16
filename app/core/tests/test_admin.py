from django.contrib.auth import get_user_model
from django.test import Client, TestCase  # Client: test request in the application for unit test
from django.urls import reverse  # generate urls for django admin page


class AdminSiteTests(TestCase):
    """Contains unit test for the admin page"""

    def setUp(self):
        """test ran before any other test"""
        # client variable accessible for other test cases
        self.client = Client()
        # admin user
        self.admin_user = get_user_model().objects.create_superuser(email="super@mail.com", password="test123")
        # uses the client to login the admin user
        self.client.force_login(self.admin_user)
        # regular user
        self.user = get_user_model().objects.create_user(email="a@mail.com", password="test123")

    def test_users_listed(self):
        """Test that users are listed on user page"""
        #  /admin/core/user/
        url = reverse("admin:core_user_changelist")
        # <TemplateResponse status_code=200, "text/html; charset=utf-8">
        res = self.client.get(url)

        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        # /admin/core/user/1
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        # /admin/core/user/add/
        url = reverse("admin:core_user_add")
        # <TemplateResponse status_code=200, "text/html; charset=utf-8">
        res = self.client.get(url)
        print(f"url: {url}\nresponse: {res}")

        self.assertEqual(res.status_code, 200)
