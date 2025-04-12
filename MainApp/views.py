from django.shortcuts import render, redirect
from django.http import JsonResponse
from MainApp.models import Product, Wishlist
from MainApp.models import Cart
from django.db.models import Q
from django.views import View
from django.shortcuts import get_object_or_404
from RatingAndReview.views import ProductReview
from django.db.models import Avg
from django.contrib.auth.decorators import login_required

from django.contrib import messages

# Create your views here.
from MainApp.models import Contact

def home(request):
    return render(request, 'MainApp/Home.html')


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


def emptyCart(request):
    return render(request, 'MainApp/emptycart.html')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        if cart_product:
            for p in cart_product:

                temp_amount = (p.quantity*p.product.discount_price)
                amount += temp_amount
                total_amount = amount+shipping_amount
            return render(request, 'MainApp/addtocart.html', {'carts': cart, 'total_amount': total_amount, 'amount': amount})
        else:
            return render(request, 'MainApp/emptycart.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()

        # Recalculate cart totals
        shipping_amount = 10.0
        cart_items = Cart.objects.filter(user=request.user)
        amount = sum(item.quantity * item.product.discount_price for item in cart_items)

        data = {
            'quantity': c.quantity,
            'item_total': c.quantity * c.product.discount_price,
            'amount': amount,
            'total_amount': amount + shipping_amount,
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))

        if c.quantity > 1:
            c.quantity -= 1
            c.save()

        # Recalculate cart totals
        shipping_amount = 10.0
        cart_items = Cart.objects.filter(user=request.user)
        amount = sum(item.quantity * item.product.discount_price for item in cart_items)

        data = {
            'quantity': c.quantity,
            'item_total': c.quantity * c.product.discount_price,
            'amount': amount,
            'total_amount': amount + shipping_amount,
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 10.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            amount += (p.quantity*p.product.discount_price)
        data = {
            'amout': amount,
            'total_amount': amount+shipping_amount
        }
        return JsonResponse(data)


@login_required
def buy_now(request, pk):
    buy_now_product = Product.objects.filter(id=pk)
    context = {'buy_now_product': buy_now_product}
    return render(request, 'MainApp/buy.html', context)


class ProductDetailsView(View):
    def get(self, request, pk):
        # Get the product by its pk
        product = get_object_or_404(Product, id=pk)

        # Fetch all reviews for this product
        reviews = ProductReview.objects.filter(product=product)

        # Calculate average rating for this product
        # Defaults to 0 if no reviews exist
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

        # Check if the product is already in the user's cart
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()

        # Prepare context with reviews, avg_rating, and item_already_in_cart
        context = {
            'product': product,
            'reviews': reviews,
            'avg_rating': avg_rating,
            'item_already_in_cart': item_already_in_cart,
        }

        return render(request, 'MainApp/productdetail.html', context)


class ToggleWishListView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        in_wishlist = Wishlist.objects.filter(
            user=request.user, product=product).exists()

        return render(request, 'MainApp/partials/wishlist_button.html', {'berverage': product, 'in_wishlist': in_wishlist})

    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user, product=product)
        if not created:
            wishlist_item.delete()
            in_wishlist = False
        else:
            in_wishlist = True
        return render(request, 'MainApp/partials/wishlist_button.html', {'berverage': product, 'in_wishlist': in_wishlist})


# ---------------------------------Price Filter -----------------------------------------------------------

def priceFilter(request, category_slug):
    if request.method == 'GET':
        min_price = request.GET.get('minprice', 1)
        max_price = request.GET.get('maxprice', 100000)
        try:
            min_price = int(min_price)
            max_price = int(max_price)
        except ValueError:
            min_price = 1
            max_price = 100000
        print(max_price, min_price)
        price_filtered_product = Product.objects.filter(
            category=category_slug, discount_price__gte=min_price, discount_price__lte=max_price)
        return render(request, 'MainApp/FilteredItems/vegs.html', {'vegetables': price_filtered_product})

def price_filter_all_product(request):
     if request.method == 'GET':
        min_price = request.GET.get('minprice', 1)
        max_price = request.GET.get('maxprice', 100000)
        try:
            min_price = int(min_price)
            max_price = int(max_price)
        except ValueError:
            min_price = 1
            max_price = 100000
        print(max_price, min_price)
        price_filtered_all_product = Product.objects.filter( discount_price__gte=min_price, discount_price__lte=max_price)
        return render(request, 'MainApp/Home.html', {'All_products':price_filtered_all_product})




def product_search(request):
    query = request.GET.get('q')
    results = Product.objects.none()

    if query:
        results = Product.objects.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query)
        )

    return render(request, 'MainApp/Home.html', {'All_products': results, 'query': query})


def product_autocomplete(request):
    if 'term' in request.GET:
        query = request.GET.get('term')
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query)
        )[:10]
        suggestions = list(products.values('title'))
        return JsonResponse(suggestions, safe=False)

def contact(request):
    if request.method == 'POST':
        # Extract form data from POST request
        full_name = request.POST.get('full_name')
        gmail = request.POST.get('gmail')
        phone_number = request.POST.get('phone_number')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save the data into the Contact model
        contact = Contact(
            full_name=full_name,
            gmail=gmail,
            phone_number=phone_number,
            subject=subject,
            message=message
        )
        contact.save()

        # After saving the data, redirect or show success message
        return redirect('contact')  # Or redirect to a thank you page

    return render(request, 'MainApp/contact.html')
# ----------------------------------------------Flitering products by category---------------------------------------------------------


def vegs(request):
    return render(request, 'MainApp/FilteredItems/vegs.html')


def beverage(request):
    return render(request, 'MainApp/FilteredItems/beverage.html')


def proteins(request):
    return render(request, 'MainApp/FilteredItems/proteins.html')


def instantfood(request):
    return render(request, 'MainApp/FilteredItems/instantfood.html')


def dairy(request):
    return render(request, 'MainApp/FilteredItems/dairy.html')


def pickle(request):
    return render(request, 'MainApp/FilteredItems/pickleandjams.html')


def fruits(request):
    return render(request, 'MainApp/FilteredItems/fruits.html')


def grocery(request):
    return render(request, 'MainApp/FilteredItems/grocery.html')


def wishList(request):
    return render(request, 'MainApp/FilteredItems/wishlist.html')

def das(request):
    return render(request,'MainApp/FilteredItems/das.html')