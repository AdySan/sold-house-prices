from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = ''
    help = ('Load house sales data from a CSV and save it into DB')

    def handle(self, *args, **options):
        pass
