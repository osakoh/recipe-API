"""
Mocking: change the behaviour of the dependencies of the code to be tested.
- Change behaviour of dependencies
- Avoid unintended side effects
- Isolate the code to be tested

Importance of mocking:
- Never write test that depend on external services
- So you don't send spam emails
"""

from unittest.mock import patch  # mocks the Django getDatabase function

from django.core.management import call_command  # Django's call_command
from django.db.utils import OperationalError  # Django's OperationalError when the database is not available
from django.test import TestCase


class CommandTests(TestCase):
    """Test the custom command functions"""

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        # retrieves the default database from "django.db.utils.ConnectionHandler.__getitem__"
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            # overrides the connection function to return True and monitor the number of times it was called
            gi.return_value = True
            # wait_for_db: the name of the management command
            call_command("wait_for_db")
            self.assertEqual(gi.call_count, 1)

    # @patch removes the 1 sec delay if an operational error is returned to speed up the test
    @patch("time.sleep", return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            # [OperationalError] * 5: raises the OperationalError 5 times
            #  + [True]: returns True on the 6th time
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command("wait_for_db")
            # connection to DB is successful on the 6th try, no OperationalError is raised
            self.assertEqual(gi.call_count, 6)
