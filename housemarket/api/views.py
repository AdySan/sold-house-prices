from django.shortcuts import render
from django.db.models import Avg

from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

from housesales.models import HouseSales

def _filter_sales(request):
    postcode = request.query_params.get('postcode', None)

    date_init_str = request.query_params.get('date_init', None)
    date_init = datetime.strptime(date_init_str, '%Y-%m-%d').date() if date_init_str else None

    date_stop_str = request.query_params.get('date_stop', None)
    date_stop = datetime.strptime(date_stop_str, '%Y-%m-%d').date() if date_stop_str else None

    sales = HouseSales.objects.all()

    if postcode:
        sales = sales.filter(postcode__contains=postcode)
    if date_init:
        sales = sales.filter(date_of_transfer__gte=date_init)
    if date_stop:
        sales = sales.filter(date_of_transfer__lte=date_stop)

    return sales

class AvgPricesView(APIView):
    def get(self, request, format=None):
        sales = _filter_sales(request)
        sales = sales.values('property_type', 'date_of_transfer').order_by('date_of_transfer').annotate(price_avg=Avg('price'))
        return Response({'sales': sales})

class TransactionsPriceBrackets(APIView):
    def _find_min(self, sales):
        min_price = None

        for s in sales:
            if min_price is None:
                min_price = s.price
            else:
                min_price = s.price if s.price < min_price else min_price

        return min_price

    def _find_max(self, sales):
        max_price = None

        for s in sales:
            if max_price is None:
                max_price = s.price
            else:
                max_price = s.price if s.price > max_price else max_price

        return max_price

    def _count_transactions_in_price_range(self, sales, start_price, end_price, include_start=True, include_end=True):
        count = 0

        for s in sales:
            if include_start:
                if include_end:
                    if s.price >= start_price and s.price <= end_price:
                        count += 1
                else:
                    if s.price >= start_price and s.price < end_price:
                        count += 1
            else:
                if include_end:
                    if s.price > start_price and s.price <= end_price:
                        count += 1
                else:
                    if s.price > start_price and s.price < end_price:
                        count += 1

        return count

    def get(self, request, format=None):
        sales = _filter_sales(request)
        number_of_chunks = int(request.query_params.get('number_of_chunks', 8))

        min_price = self._find_min(sales)
        max_price = self._find_max(sales)

        chunk_size = (max_price - min_price) // number_of_chunks

        chunks = range(min_price, max_price, chunk_size)
        transactions_brackets = []

        for i, c in enumerate(chunks):
            include_end = (i == len(chunks) -1)
            transactions_brackets.append(self._count_transactions_in_price_range(
                sales,
                c,
                c + chunk_size,
                include_start=True,
                include_end=include_end))

        return Response({'total_transactions': sales.count(),
                        'min_price': min_price,
                        'max_price': max_price,
                        "transactions_brackets": transactions_brackets})
