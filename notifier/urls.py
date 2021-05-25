from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('getPin', views.getPin, name='pin'),
    path('addOrder', views.addOrder, name='add'),
    path('getLog', views.getOrder, name='order'),
    
]