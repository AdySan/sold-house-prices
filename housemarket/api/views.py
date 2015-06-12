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
        sales = sales.filter(date_of_transfer__lt=date_stop)

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

        min_price = self._find_min(sales)
        max_price = self._find_max(sales)

        chunk_size = (max_price - min_price) // 8

        chunk_1_start = min_price
        chunk_2_start = chunk_1_start + chunk_size
        chunk_3_start = chunk_2_start + chunk_size
        chunk_4_start = chunk_3_start + chunk_size
        chunk_5_start = chunk_4_start + chunk_size
        chunk_6_start = chunk_5_start + chunk_size
        chunk_7_start = chunk_6_start + chunk_size
        chunk_8_start = chunk_7_start + chunk_size

        transactions_in_bracket_1 = self._count_transactions_in_price_range(sales, chunk_1_start, chunk_2_start, include_start=True, include_end=False)
        transactions_in_bracket_2 = self._count_transactions_in_price_range(sales, chunk_2_start, chunk_3_start, include_start=True, include_end=False)
        transactions_in_bracket_3 = self._count_transactions_in_price_range(sales, chunk_3_start, chunk_4_start, include_start=True, include_end=False)
        transactions_in_bracket_4 = self._count_transactions_in_price_range(sales, chunk_4_start, chunk_5_start, include_start=True, include_end=False)
        transactions_in_bracket_5 = self._count_transactions_in_price_range(sales, chunk_5_start, chunk_6_start, include_start=True, include_end=False)
        transactions_in_bracket_6 = self._count_transactions_in_price_range(sales, chunk_6_start, chunk_7_start, include_start=True, include_end=False)
        transactions_in_bracket_7 = self._count_transactions_in_price_range(sales, chunk_7_start, chunk_8_start, include_start=True, include_end=False)
        transactions_in_bracket_8 = self._count_transactions_in_price_range(sales, chunk_8_start, max_price, include_start=True, include_end=True)

        return Response({'total_transactions': sales.count(),
                        'min_price': min_price,
                        'max_price': max_price,
                        'transactions_in_bracket_1': transactions_in_bracket_1,
                        'transactions_in_bracket_2': transactions_in_bracket_2,
                        'transactions_in_bracket_3': transactions_in_bracket_3,
                        'transactions_in_bracket_4': transactions_in_bracket_4,
                        'transactions_in_bracket_5': transactions_in_bracket_5,
                        'transactions_in_bracket_6': transactions_in_bracket_6,
                        'transactions_in_bracket_7': transactions_in_bracket_7,
                        'transactions_in_bracket_8': transactions_in_bracket_8})
