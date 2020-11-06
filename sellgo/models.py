from django.db import models

# Create your models here.

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, default='Test Name')
    email = models.CharField(max_length=254,blank=False, default='test@example.com')
    created_date = models.DateTimeField(auto_now_add=True)


class Csv_product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500, blank=False, default='Test Title')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    uploaded_date = models.DateTimeField(auto_now=True)
