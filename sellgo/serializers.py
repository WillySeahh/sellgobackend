from rest_framework import serializers 
from sellgo.models import Customer
from sellgo.models import Csv_product

class CustomerSerializer(serializers.ModelSerializer):
        class Meta:
            model = Customer
            fields = ('id',
                    'name',
                    'email',
                    'created_date')

class CSVSerializer(serializers.ModelSerializer):
    class Meta:
        model = Csv_product
        fields = ('id',
                'title',
                'price',
                'customer_id',
                'uploaded_date')
