from rest_framework import serializers
from notifier.models import Order,Pin

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'

class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model=Pin
        fields='__all__'