import time

from django.core.management.base import BaseCommand  # class for creating a Django custom command
from django.db.utils import OperationalError  # error thrown if the database connection is not available
from psycopg2 import OperationalError as Psycopg2Error


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        # args: ()
        # options: {'verbosity': 1, 'settings': None, 'pythonpath': None, 'traceback': False, 'no_color': False, 'force_color': False, 'skip_checks': True}
        # printing to the screen
        self.stdout.write(self.style.WARNING("\nWaiting for database....\n"))
        # boolean: assume the db is not ready
        db_conn = False
        # if no database connection
        while db_conn is False:
            # try connecting to the default database
            try:
                # if db isn't ready;it throws either one of the exceptions(jumps to except block) skipping the next line
                self.check(databases=["default"])
                # no exception raised, meaning the db is ready
                # stops the while loop; jumping to 'self.stdout.write(self.style.SUCCESS'
                db_conn = True
            # cannot connect to the default database
            except (Psycopg2Error, OperationalError):
                self.stdout.write("Database unavailable: Can't connect to the default database, waiting 1 second...")
                # pause execution for 1 second
                time.sleep(1)
        # printing message colored green to the screen
        self.stdout.write(self.style.SUCCESS("\n+++++++++++++++++ Database available! +++++++++++++++++ \n"))


"""
Before while: db_conn: None
In try catch: db_conn: None
Database unavailable, waiting 1 second...
In try catch: db_conn: None
Database unavailable, waiting 1 second...
In try catch: db_conn: None
Database unavailable, waiting 1 second...
In try catch: db_conn: None
Database unavailable, waiting 1 second...
In try catch: db_conn: None
Database unavailable, waiting 1 second...
In try catch: db_conn: None
Same line as while: db_conn: True
"""
