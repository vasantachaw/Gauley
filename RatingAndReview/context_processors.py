from RatingAndReview.models import OverallReview
from RatingAndReview.models import ProductReview
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from RatingAndReview.models import Product



def avg_rating(request):
    reviews = OverallReview.objects.all().order_by('?')
    context={'Overall_review':reviews}
    
    return context


def product_rating_context(request):
    average_rating = OverallReview.objects.aggregate(Avg('rating'))['rating__avg']
    context={'avge_rating':average_rating}
    return context
