from django.contrib import admin
from RatingAndReview.models import ProductReview
from RatingAndReview.models import OverallReview
# Register your models here.

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    search_fields = ('product__title', 'user__username')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)


@admin.register(OverallReview)
class OverallReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment','rating', 'created_at')
    
    
