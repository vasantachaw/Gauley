from django.shortcuts import render, redirect, HttpResponse
from MainApp.models import Customer
from MainApp.models import Cart
from MainApp.models import OrderPlaced
from MainApp.models import Product
import requests
import uuid
import hashlib
import base64
import hmac


def checkout(request):
    return render(request, 'paymentgateway/checkout.html')


def orders(request):
    return render(request, 'paymentgateway/orders.html')


def payment_done(request):
    # Fetch the customer related to the logged-in user
    customer = Customer.objects.filter(user=request.user).first()
    
    if not customer:
        return HttpResponse("Customer profile not found. Please complete your profile.")

    # Get all items in the cart for the logged-in user
    cart = Cart.objects.filter(user=request.user)
    
    # Process each item in the cart and create an order
    for c in cart:
        # Get the product associated with the cart item
        product = c.product
        
        # Check if there's enough stock available
        if product.stock >= c.quantity:
            # Create an order for each item in the cart
            OrderPlaced.objects.create(
                user=request.user, 
                customer=customer, 
                product=product, 
                quantity=c.quantity
            )
            
            # Decrease the stock by the quantity of the order
            product.stock -= c.quantity
            product.save()  # Save the updated stock

            # Remove the item from the cart after the order is placed
            c.delete()  # Cart item is removed after the order is placed
        else:
            # If there’s not enough stock, return a message or handle accordingly
            return HttpResponse(f"Not enough stock for {product.title}. Order could not be placed.")
    
    # Redirect to the home page after successful payment
    return redirect('home')


def integrate(request):
    # Retrieve cart items from session
    cart_items = Cart.objects.filter(user=request.user)
    cart_details = []
    for cart_item in cart_items:
        subtotal = cart_item.total_cost  # Using the total_cost property
        cart_details.append({
            'product': cart_item.product,
            'quantity': cart_item.quantity,
            'discount_price': cart_item.product.discount_price,
            'subtotal': subtotal,
        })
        total_cart_amount += subtotal  # Add to the total cart amount

    print(cart_item)

    # Calculate grand total
    grand_total = sum(item['total'] for item in cart_items)

    # Generate a UUID for the transaction
    transaction_uuid = uuid.uuid4()
    transaction_uuid_hex = transaction_uuid.hex

    # Define the SecretKey provided by eSewa
    secret_key = "8gBm/:&EnhH.1/q"

    # Calculate the signature using HMAC-SHA256
    signature_data = f'total_amount={grand_total},transaction_uuid={transaction_uuid_hex},product_code=EPAYTEST'
    signature = hmac.new(secret_key.encode(),
                         signature_data.encode(), hashlib.sha256)
    signature = base64.b64encode(signature.digest()).decode()

    # Construct the eSewa form data
    esewa_data = {
        'amount': grand_total,
        'total_amount': grand_total,
        'signature': signature,
        'transaction_uuid': transaction_uuid_hex,
    }

    # Add esewa_data to the template context
    context = {'esewa_data': esewa_data}
    print(esewa_data)

    return render(request, 'integrate.html', context)


def khalti_payment(request):
    # Generate a UUID for the transaction
    transaction_uuid = uuid.uuid4()

    # Retrieve grand total from session
    grand_total = request.session.get('grand_total', 0)

    # Convert grand total to paisa (assuming grand total is in rupees)
    amount = grand_total  # Convert rupees to paisa

    context = {
        'purchase_order_id': transaction_uuid,
        'amount': amount,
    }

    return render(request, 'khalti_payment.html', context)


def submit_khalti_payment(request):
    customer = Customer.objects.filter(user=request.user).first()
    if not customer:
        return redirect('profile')

    if request.method == 'POST':
        # Retrieve data from the POST request
        return_url = request.POST.get('return_url')
        product_service_charge = int(request.POST.get(
            'product_service_charge'))  # Service charge
        product_delivery_charge = int(request.POST.get(
            'product_delivery_charge'))  # Delivery charge

        cart_items = Cart.objects.filter(user=request.user)

        # Create a list of cart details, including the subtotal for each product
        cart_details = []
        product_details = []
        total_cart_amount = 0  # Initialize the total amount variable

        for cart_item in cart_items:
            subtotal = cart_item.total_cost  # Using the total_cost property

            # Store detailed cart info (for debugging or display)
            cart_details.append({
                'product': cart_item.product,
                'quantity': cart_item.quantity,
                'discount_price': cart_item.product.discount_price,
                'subtotal': subtotal,
            })

            # Add to product_details for Khalti payload
            product_details.append({
                "identity": str(cart_item.product.id),
                "name": cart_item.product.title,
                "total_price": int(subtotal * 100),  # Convert to paisa
                "quantity": cart_item.quantity,
                # Convert to paisa
                "unit_price": int(cart_item.product.discount_price * 100)
            })

            # Calculate total cart amount
            total_cart_amount += subtotal

        print('------------------------------------------------')
        print(cart_details)

        # Extracting charges from the request
        product_service_charge = int(
            request.POST.get('product_service_charge', 0))
        product_delivery_charge = int(
            request.POST.get('product_delivery_charge', 0))

        # Ensure all amounts are in paisa (NPR)
        total_amount = (total_cart_amount +
                        product_service_charge + product_delivery_charge) * 100

        # Construct payload for Khalti payment initiation
        payload = {
            "return_url": return_url,
            "website_url": "http://localhost:8000",  # Your website URL
            "amount": total_amount,  # Total amount in paisa
            # Order ID (must be a string)
            "purchase_order_id": str(uuid.uuid4()),
            "purchase_order_name": "Test Product",
            "customer_info": {
                "name": "Ram Bahadur",
                "email": "test@khalti.com",
                "phone": "9800000001"
            },
            "amount_breakdown": [
                {
                    "label": "Product Price",
                    "amount": total_cart_amount * 100
                },
                {
                    "label": "Service Charge",
                    "amount": product_service_charge * 100
                },
                {
                    "label": "Delivery Charge",
                    "amount": product_delivery_charge * 100
                }
            ],
            "product_details": product_details,
            "merchant_username": "merchant_name",
            "merchant_extra": "merchant_extra"
        }

        # Headers for Khalti API request
        headers = {
            'Authorization': 'key dbcbaa1451ec4e0fa6543ba2e694481d',
            'Content-Type': 'application/json',
        }

        # Khalti API endpoint for payment initiation
        url = "https://a.khalti.com/api/v2/epayment/initiate/"

        # Make a POST request to initiate Khalti payment
        response = requests.post(url, headers=headers, json=payload)

        # Print response text for debugging (you can remove this in production
        print(response.text)

        # If response is successful, it will return the payment URL
        if response.status_code == 200:
            new_res = response.json()  # Parse the JSON response
            print("Payment initiation successful.")
            # You can redirect to this URL for payment
            print("Payment URL:", new_res.get('payment_url'))
            # cart = Cart.objects.filter(user=request.user)
            # for c in cart:
            #     OrderPlaced.objects.create(
            #         user=request.user, customer=customer, product=c.product, quantity=c.quantity
            #     )
            #     c.delete()

            # Redirect to Khalti payment URL
            return redirect(new_res['payment_url'])
        else:
            print("Error occurred in Khalti payment initiation.")
            print(f"Error Details: {response.text}")
            return HttpResponse("Failed to initiate payment.")
    else:
        return HttpResponse("Invalid Request")


def khalti_payment(request):
    # Generate a UUID for the transaction
    transaction_uuid = uuid.uuid4()

    # Retrieve grand total from session
    grand_total = request.session.get('grand_total', 0)

    # Convert grand total to paisa (assuming grand total is in rupees)
    amount = grand_total  # Convert rupees to paisa

    context = {
        'purchase_order_id': transaction_uuid,
        'amount': amount,
    }

    return render(request, 'khalti_payment.html', context)
