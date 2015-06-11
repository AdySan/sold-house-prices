from django.shortcuts import render
from django.db.models import Avg

from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

from housesales.models import HouseSales


class AvgPricesView(APIView):
    def get(self, request, format=None):
        date_init = datetime.strptime('2015-01-01', '%Y-%m-%d').date()
        date_stop = datetime.strptime('2015-02-28', '%Y-%m-%d').date()

        # SELECT avg(price), property_type, date_of_transfer
        #     FROM housesales_housesales
        #     WHERE date_of_transfer >= '2015-01-01' AND date_of_transfer < '2015-02-28'
        #     GROUP BY property_type, date_of_transfer
        #     ORDER BY timee_of_transfer

        sales = HouseSales.objects.filter(
            date_of_transfer__gte=date_init, date_of_transfer__lt=date_stop, postcode__contains='SE13').values(
            'property_type', 'date_of_transfer').order_by(
            'date_of_transfer').annotate(
            price_avg=Avg('price'))
        return Response({'sales': sales})
