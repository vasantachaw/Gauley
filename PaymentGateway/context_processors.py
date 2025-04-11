from django.shortcuts import render, redirect, HttpResponse
from MainApp.models import Customer
from MainApp.models import Cart
from MainApp.models import OrderPlaced


def payment_details(request):
    if request.user.is_authenticated:
       
        orders = OrderPlaced.objects.filter(user=request.user)
       
        context = {
            'orders': orders,
            #'app_status':appointments
        }
    else:
        context = {
            'orders': '',   
        }
    
    return context

def pay_customer_details(request):
    pay_details = None  # Default value

    if request.user.is_authenticated:
        pay_details = Customer.objects.filter(user=request.user)
    
    context = {'pay_details': pay_details}
    return context
