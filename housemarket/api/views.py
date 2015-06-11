from django.shortcuts import render
from django.db.models import Avg

from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

from housesales.models import HouseSales


class AvgPricesView(APIView):
    def get(self, request, format=None):
        postcode = self.request.query_params.get('postcode', None)

        date_init_str = self.request.query_params.get('date_init', None)
        date_init = datetime.strptime(date_init_str, '%Y-%m-%d').date() if date_init_str else None

        date_stop_str = self.request.query_params.get('date_stop', None)
        date_stop = datetime.strptime(date_stop_str, '%Y-%m-%d').date() if date_stop_str else None

        sales = HouseSales.objects.all()

        if postcode:
            sales = sales.filter(postcode__contains=postcode)
        if date_init:
            sales = sales.filter(date_of_transfer__gte=date_init)
        if date_stop:
            sales = sales.filter(date_of_transfer__lt=date_stop)

        sales = sales.values('property_type', 'date_of_transfer').order_by('date_of_transfer').annotate(price_avg=Avg('price'))

        return Response({'sales': sales})
