from django.db.models import Avg
from MainApp.models import Product, Cart, Wishlist
from RatingAndReview.models import ProductReview
from django.db.models import Sum

def product_filter_view(request):
    # Filter all products except specific categories
    all_products = Product.objects.exclude(category__in=['Banner', 'OffSeasonal', 'OnSeasonal']).order_by('?')[:30]

    # Annotate each product with its average rating from ProductReview
    all_products = all_products.annotate(average_rating=Avg('reviews__rating'))

    # Filter products by category and annotate them with the average rating
    vegetables = Product.objects.filter(category='Vegetables').annotate(average_rating=Avg('reviews__rating')).order_by('?')
    beverages = Product.objects.filter(category='Beverages').annotate(average_rating=Avg('reviews__rating')).order_by('?')
    proteins = Product.objects.filter(category='Proteins').annotate(average_rating=Avg('reviews__rating')).order_by('?')
    instantfood = Product.objects.filter(category='InstantFoods').annotate(average_rating=Avg('reviews__rating')).order_by('?')
    dairy = Product.objects.filter(category='DairyBakery').annotate(average_rating=Avg('reviews__rating')).order_by('?')
    pickle = Product.objects.filter(category='PicklesJams').annotate(average_rating=Avg('reviews__rating')).order_by('?')
    fruits = Product.objects.filter(category='Fruits').annotate(average_rating=Avg('reviews__rating')).order_by('?')
    banner = Product.objects.filter(category='Banner').annotate(average_rating=Avg('reviews__rating')).order_by('?')
    off = Product.objects.filter(category='OffSeasonal').annotate(average_rating=Avg('reviews__rating'))
    onn = Product.objects.filter(category='OnSeasonal').annotate(average_rating=Avg('reviews__rating'))
    grocery = Product.objects.filter(category='Grocery').annotate(average_rating=Avg('reviews__rating')).order_by('?')

    total_products_count = Product.objects.count()

    # Fetch the latest products ordered by created_at (newest first)
    latest_products = Product.objects.annotate(average_rating=Avg('reviews__rating')).order_by('-created_at')[:10]

    # Get all products ordered by the highest rating
    popular = Product.objects.annotate(average_rating=Avg('reviews__rating')).order_by('-average_rating')


    # Initialize context variables
    context = {
        'All_products': all_products,
        'vegetables': vegetables,
        'beverages': beverages,
        'Proteins': proteins,
        'instantfood': instantfood,
        'dairy': dairy,
        'pickle': pickle,
        'fruits': fruits,
        'banner': banner,
        'off': off,
        'on': onn,
        'grocery': grocery,
        'total_products': total_products_count,
        'latest_products': latest_products,
        'papular':popular,
    }

    # Add cart and wishlist info if user is authenticated
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = cart_items.count()
        total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_cart_amount = sum(item.total_cost for item in cart_items)

        total_wishlist_items = Wishlist.objects.filter(user=request.user).count()
        fav = Wishlist.objects.filter(user=request.user).order_by('?')

        cart_details = [
            {
                'product': cart_item.product,
                'quantity': cart_item.quantity,
                'discount_price': cart_item.product.discount_price,
                'subtotal': cart_item.total_cost,
            }
            for cart_item in cart_items
        ]

        context.update({
            'cart_count': cart_count,
            'qty': total_quantity,
            'cart_details': cart_details,
            'total_cart_amount': total_cart_amount,
            'total_wishlist_items': total_wishlist_items,
            'fav': fav,
        })
    else:
        context.update({
            'cart_count': 0,
            'qty': 0,
            'cart_details': [],
            'total_cart_amount': 0,
            'total_wishlist_items': 0,
            'fav': 0,
        })

    # Rendering the template with context
    return context
