import time

from django.core.management.base import BaseCommand  # class for creating a Django custom command
from django.db import connections  # test if the database connection is available
from django.db.utils import OperationalError  # error thrown if the database connection is not available


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        # printing to the screen
        self.stdout.write(self.style.WARNING("\nWaiting for database....\n"))
        db_conn = None
        # if no database connection
        while not db_conn:
            # try connecting to the default database
            try:
                db_conn = connections["default"]
            # cannot connect to the default database
            except OperationalError:
                self.stdout.write("Database unavailable, waiting 1 second...")
                # pause execution for 1 second
                time.sleep(1)
        # printing message colored green to the screen
        self.stdout.write(self.style.SUCCESS("\n+++++++++++++++++ Database available! +++++++++++++++++ \n"))
