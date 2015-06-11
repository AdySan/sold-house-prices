from django.db import models

class HouseSales(models.Model):
    transaction_id = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    date_of_transfer = models.DateField()
    postcode = models.CharField(max_length=10)
    property_type = models.CharField(max_length=1)
    old_new = models.CharField(max_length=1)
    duration = models.CharField(max_length=1)
    paon = models.CharField(max_length=250)
    saon = models.CharField(max_length=250)
    street = models.CharField(max_length=250)
    locality = models.CharField(max_length=250)
    town_city = models.CharField(max_length=250)
    district = models.CharField(max_length=250)
    county = models.CharField(max_length=250)
    status = models.CharField(max_length=1)
