from django.shortcuts import render, redirect,get_object_or_404
from RatingAndReview.models import OverallReview
from RatingAndReview.models import ProductReview
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from MainApp.models import Product
from django.db.models import Avg

@login_required(login_url='login')
def overReview(request):
    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        rating = request.POST.get('rating', '').strip()

        if  not rating:
            return HttpResponse("Missing required fields", status=400)

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError("Invalid rating")
        except ValueError:
            return HttpResponse("Invalid rating value", status=400)

        # Save review
        review = OverallReview.objects.create(
            user=request.user if request.user.is_authenticated else None,  
            rating=rating,
            comment=message,
        )
        review.save()

        return redirect('home')  # Redirect after saving

    return redirect('home')

@login_required(login_url='login')
def productReview(request, pk):
    product = get_object_or_404(Product, id=pk)

    # Check if the user has already reviewed this product
    if ProductReview.objects.filter(product=product, user=request.user).exists():
        return HttpResponse("You have already reviewed this product. You cannot submit another review.", status=400)

    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        rating = request.POST.get('rating', '').strip()

        if not rating:
            return HttpResponse("Missing required fields", status=400)

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError("Invalid rating")
        except ValueError:
            return HttpResponse("Invalid rating value", status=400)

        # Save new review if the user hasn't reviewed this product before
        ProductReview.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=message,
        )

        return redirect('product_detail', pk=product.id)  # Redirect to product page

    return redirect('product_detail', pk=product.id)  

