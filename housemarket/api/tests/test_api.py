from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from django.test import TestCase
from .factories import HouseSalesFactory
from housesales.models import HouseSales
import datetime


class HouseSalesAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_average_prices_flats_three_groups(self):
        HouseSalesFactory.create(price=200000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=250000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=430000, date_of_transfer=datetime.date(2015, 6, 14), property_type="F")
        HouseSalesFactory.create(price=120000, date_of_transfer=datetime.date(2015, 6, 14), property_type="F")
        HouseSalesFactory.create(price=102000, date_of_transfer=datetime.date(2015, 6, 15), property_type="F")
        HouseSalesFactory.create(price=656000, date_of_transfer=datetime.date(2015, 6, 15), property_type="F")

        url = reverse('house_sales', )
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['sales']), 3, "There are 3 groups of average prices")
        self.assertEqual(response.data['sales'][0]['price_avg'], 225000, "Average price for Jun 13 is 225000")
        self.assertEqual(response.data['sales'][1]['price_avg'], 275000, "Average price for Jun 13 is 275000")
        self.assertEqual(response.data['sales'][2]['price_avg'], 379000, "Average price for Jun 13 is 379000")

    def test_get_average_prices_empty_db(self):
        url = reverse('house_sales', )
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_average_prices_filter_by_date(self):
        HouseSalesFactory.create(price=200000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=250000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=430000, date_of_transfer=datetime.date(2015, 6, 14), property_type="F")
        HouseSalesFactory.create(price=120000, date_of_transfer=datetime.date(2015, 6, 14), property_type="F")
        HouseSalesFactory.create(price=102000, date_of_transfer=datetime.date(2015, 6, 15), property_type="F")
        HouseSalesFactory.create(price=656000, date_of_transfer=datetime.date(2015, 6, 15), property_type="F")
        HouseSalesFactory.create(price=100000, date_of_transfer=datetime.date(2015, 7, 30), property_type="F")
        HouseSalesFactory.create(price=100000, date_of_transfer=datetime.date(2015, 8, 20), property_type="F")

        url = reverse('house_sales', )
        data = {'date_init': '2015-06-13', 'date_stop': '2015-06-15'}
        response = self.client.get(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['sales']), 3, "There are 3 groups of average prices between Jun 13th and Jun 15th")

    def test_get_average_prices_filter_by_postcode(self):
        HouseSalesFactory.create(price=200000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F", postcode="SWXXX")
        HouseSalesFactory.create(price=250000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F", postcode="SWXXX")
        HouseSalesFactory.create(price=430000, date_of_transfer=datetime.date(2015, 6, 14), property_type="F", postcode="SWXXX")
        HouseSalesFactory.create(price=120000, date_of_transfer=datetime.date(2015, 6, 14), property_type="F", postcode="SWXXX")
        HouseSalesFactory.create(price=102000, date_of_transfer=datetime.date(2015, 6, 15), property_type="F", postcode="SWXXX")
        HouseSalesFactory.create(price=656000, date_of_transfer=datetime.date(2015, 6, 15), property_type="F", postcode="SWXXX")
        HouseSalesFactory.create(price=100000, date_of_transfer=datetime.date(2015, 6, 14), property_type="F", postcode="SEXXX")
        HouseSalesFactory.create(price=100000, date_of_transfer=datetime.date(2015, 6, 14), property_type="F", postcode="SEXXX")

        url = reverse('house_sales', )
        data = {'postcode': 'SW'}
        response = self.client.get(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['sales']), 3, "There are 3 groups of average prices with postcode starting for SW")

    def test_get_average_prices_filter_by_postcode_and_date(self):
        HouseSalesFactory.create(price=200000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F", postcode="SWXXX")
        HouseSalesFactory.create(price=250000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F", postcode="SWXXX")
        HouseSalesFactory.create(price=430000, date_of_transfer=datetime.date(2015, 6, 14), property_type="F", postcode="SWXXX")
        HouseSalesFactory.create(price=120000, date_of_transfer=datetime.date(2015, 6, 14), property_type="F", postcode="SWXXX")
        HouseSalesFactory.create(price=102000, date_of_transfer=datetime.date(2015, 6, 15), property_type="F", postcode="SWXXX")
        HouseSalesFactory.create(price=656000, date_of_transfer=datetime.date(2015, 6, 15), property_type="F", postcode="SWXXX")
        HouseSalesFactory.create(price=100000, date_of_transfer=datetime.date(2015, 8, 14), property_type="F", postcode="SEXXX")
        HouseSalesFactory.create(price=100000, date_of_transfer=datetime.date(2015, 6, 14), property_type="F", postcode="SEXXX")

        url = reverse('house_sales', )
        data = {'postcode': 'SW'}
        response = self.client.get(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['sales']), 3, "There are 3 groups of average prices with postcode starting for SW and in the specified date range")

    def test_get_price_brackets_count(self):
        HouseSalesFactory.create(price=100000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=120000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=130000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=135000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=220000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=230000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=330000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=335000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=340000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=420000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=510000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=520000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=650000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=660000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=730000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=735000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=740000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=750000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=860000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")
        HouseSalesFactory.create(price=900000, date_of_transfer=datetime.date(2015, 6, 13), property_type="F")

        url = reverse('house_transactions', )
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_transactions'], 20)
        self.assertEqual(response.data['min_price'], 100000)
        self.assertEqual(response.data['max_price'], 900000)
        self.assertEqual(response.data['transactions_in_bracket_1'], 4)
        self.assertEqual(response.data['transactions_in_bracket_2'], 2)
        self.assertEqual(response.data['transactions_in_bracket_3'], 3)
        self.assertEqual(response.data['transactions_in_bracket_4'], 1)
        self.assertEqual(response.data['transactions_in_bracket_5'], 2)
        self.assertEqual(response.data['transactions_in_bracket_6'], 2)
        self.assertEqual(response.data['transactions_in_bracket_7'], 4)
        self.assertEqual(response.data['transactions_in_bracket_8'], 2)
