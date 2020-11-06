from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework_csv.parsers import CSVParser
from rest_framework_csv.renderers import CSVRenderer

from sellgo.models import Customer
from sellgo.models import Csv_product
from sellgo.serializers import CustomerSerializer
from sellgo.serializers import CSVSerializer
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict


import csv 
import json 

# Create your views here.

@api_view(['GET', 'POST', 'DELETE'])
def customer_list(request):
    # GET list of customers, POST a new customer, DELETE all customers
    if request.method == 'GET':
        customers = Customer.objects.all()   
        customers_serializer = CustomerSerializer(customers, many=True)
        return JsonResponse(customers_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        customer_data = JSONParser().parse(request)
        customer_serializer = CustomerSerializer(data=customer_data)
        if customer_serializer.is_valid():
            customer_serializer.save()
            return JsonResponse(customer_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Customer.objects.all().delete()
        return JsonResponse({'message': '{} Customers were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def customer_detail(request, pk):
    # find customer by pk (id)
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return JsonResponse({'message': 'The customer does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    # GET / PUT / DELETE customer
    if request.method == 'GET':
        customer_serializer = CustomerSerializer(customer)
        return JsonResponse(customer_serializer.data)
 
    elif request.method == 'PUT':
        customer_data = JSONParser().parse(request) 
        customer_serializer = CustomerSerializer(customer, data=customer_data) 
        if customer_serializer.is_valid(): 
            customer_serializer.save() 
            return JsonResponse(customer_serializer.data) 
        return JsonResponse(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE':
        customer.delete() 
        return JsonResponse({'message': 'Customer was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST', 'DELETE'])
def csv_list(request,pk):
  
    if request.method == 'POST':
        data = {}
        # Open a csv reader called DictReader 
        with open('take_home_test_data.csv', encoding='utf-8') as csvf: 
            csvReader = csv.DictReader(csvf) 
            
            # Convert each row into a dictionary  
            # and add it to data 
            isSuccessful = True
            for rows in csvReader: 
            
                # Assuming a column named 'No' to 
                # be the primary key 
                key = rows['Title'] 
                data[key] = rows

                rows['customer_id'] = pk

                rows['title'] = rows['Title']
                del rows['Title']

                rows['price'] = rows[' Price']
                del rows[' Price']
                
                csv_serializer = CSVSerializer(data=rows)
                if csv_serializer.is_valid():
                    csv_serializer.save()
                else:
                    isSuccessful = False
            
            if (isSuccessful):       
                return JsonResponse(csv_serializer.data, status=status.HTTP_201_CREATED) 
            else:  
                return JsonResponse(csv_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'GET':
        #Getting from Csv_product table
        data = {}

        try:
            csv_product_mouse = Csv_product.objects.filter(title__contains='Apple').latest('uploaded_date') #CSV shows a weird unicode char, however I suspect it isnt ""
            csv_product_keyboard = Csv_product.objects.filter(title__contains='Keyboard').latest('uploaded_date')
            csv_product_speaker= Csv_product.objects.filter(title__contains='Speaker').latest('uploaded_date')
        except csv_product_mouse.DoesNotExist:
            return JsonResponse({'message': 'It does not exists'}, status=status.HTTP_404_NOT_FOUND) 

        csv_serializer_mouse = CSVSerializer(csv_product_mouse)
        csv_serializer_keyboard = CSVSerializer(csv_product_keyboard)
        csv_serializer_speaker = CSVSerializer(csv_product_speaker)

        data = csv_serializer_mouse.data
        data2 = csv_serializer_keyboard.data
        data3 = csv_serializer_speaker.data
        data['product_title_mouse'] = data['title']
        del data['title']
        data['product_price_mouse'] = data['price']
        del data['price']
        data['product_last_updated_mouse'] = data2['uploaded_date']
        del data['uploaded_date']


        data['product_title_keyboard'] = data2['title']
        data['product_price_keyboard'] = data2['price']
        data['product_last_updated_keyboard'] = data2['uploaded_date']

        data['product_title_speaker'] = data3['title']
        data['product_price_speaker'] = data3['price']
        data['product_last_updated_speaker'] = data3['uploaded_date']


        #Getting from Customer table
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return JsonResponse({'message': 'The customer does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            customer_serializer = CustomerSerializer(customer)
            data['customer_name'] = customer_serializer.data['name']

        return JsonResponse(data)
        



            



                
       
