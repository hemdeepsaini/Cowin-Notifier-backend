from django.db.models.fields import EmailField
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Order,Pin
from .serializer import OrderSerializer,PinSerializer

@csrf_exempt
def index(request):
    response = json.dumps([
    {
        'pinDropDown':'/getPin',
        'order':'/addOrder',
        'log':'/getLog',
    }])
    # api_urls={
        
    # }
    return HttpResponse(response, content_type='text/json')

@api_view(['GET'])
def getPin(request):
    pin = Pin.objects.all()
    response=PinSerializer(pin,many=True)
    return JsonResponse(response.data, safe=False)

@csrf_exempt
def addOrder(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        oPin = payload['pin']
        oEmail = payload['email']
        oAge = payload['age']
        oCount = 1
        order = Order(pin=oPin, email=oEmail,age=oAge,count=oCount)
        try:
            order.save()
            response = json.dumps([{ 'Success': 'Order added successfully!'}])
        except:
            response = json.dumps([{ 'Error': 'Order could not be added!'}])
    return HttpResponse(response, content_type='text/json')

@api_view(['GET'])
def getOrder(request):
    order = Order.objects.all()
    response=OrderSerializer(order,many=True)
    return JsonResponse(response.data, safe=False)
            
  