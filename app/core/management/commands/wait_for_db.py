import time

from django.db import connections
from django.db.utils import OperationalError

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Pause execution until db is available"""
    def handle(self, *args, **options):
        self.stdout.write("Waiting for database to be available")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections["default"]
            except OperationalError:
                self.stdout.write("Waiting 1s")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database is available"))
