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
from django.test import SimpleTestCase
from psycopg2 import OperationalError as Psycopg2Error


# location of function to mock
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test the custom command functions"""

    def test_wait_for_db_ready(self, patched_check):
        """
        Test waiting for db when db is ready
        patched_check: new argument added to each method due to '@patch() function
        """
        # return_value: value returned by calling the mock; by default return value is a mock object,
        # i.e.  <MagicMock name='check()' id='139639477237120'>
        patched_check.return_value = True
        # call function
        call_command("wait_for_db")
        # assert_called_with() OR assert_called_once_with(): checks that the mock was called with the correct arguments
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for db when getting OperationalError"""
        # raise Psycopg2Error twice & Django's OperationalError three times then return True
        # Psycopg2Error: Postgres hasn't started. It's not ready to accept connections
        # OperationalError: Postgres is ready to accept connection, but the test DB isn't setup/created
        # side effect - can either be a function to be called when the mock is called, an iterable or
        # an exception (class or instance) to be raised. In this test, its raises an exception when mocking
        patched_check.side_effect = [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        # call function
        call_command("wait_for_db")
        # connection to DB is successful on the 6th try, no OperationalError is raised
        # call_count: an integer that counts how many times the mock object has been called
        self.assertEqual(patched_check.call_count, 6)
        # assert_called_with() OR assert_called_once_with(): checks that the mock was called with the correct arguments
        patched_check.assert_called_with(databases=['default'])
