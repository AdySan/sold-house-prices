from django.core.management.base import BaseCommand
from django.db import transaction

from housesales.models import HouseSales

import csv
from datetime import datetime


class Command(BaseCommand):
    help = ('Load house sales data from a CSV and save it into DB')

    def add_arguments(self, parser):
        parser.add_argument('--csv', type=str)
        parser.add_argument('--postcode', type=str)
        parser.add_argument('--maxrows', type=int)

    @transaction.atomic
    def handle(self, *args, **options):
        if options['csv']:
            file_name = options['csv']
            print 'Filling house sales db with: {0}'.format(file_name)
            with open(file_name, 'rU') as f:
                reader = csv.reader(f)

                housesales = []
                max_rows = options['maxrows'] if options['maxrows'] else None
                postcode = options['postcode'] if options['postcode'] else None
                count = 0

                for row in reader:
                    if max_rows:
                        if count == max_rows:
                            break

                    hs = HouseSales()

                    hs.transaction_id = row[0][1:len(row[0]) -1]
                    hs.price = int(row[1])
                    hs.date_of_transfer = datetime.strptime(row[2], '%Y-%m-%d %H:%M').date()
                    hs.postcode = row[3]
                    hs.property_type = row[4]
                    hs.old_new = row[5]
                    hs.duration = row[6]
                    hs.paon = row[7]
                    hs.saon = row[8]
                    hs.street = row[9]
                    hs.locality = row[10]
                    hs.town_city = row[11]
                    hs.district = row[12]
                    hs.county = row[13]
                    hs.status = row[14]

                    if postcode:
                        if hs.postcode.startswith(postcode):
                            housesales.append(hs)
                            count += 1
                    else:
                        housesales.append(hs)
                        count += 1

                HouseSales.objects.bulk_create(housesales)
