from django.contrib import admin
from MainApp.models import Customer
from MainApp.models import Product
from MainApp.models import Cart
from MainApp.models import OrderPlaced,Wishlist
# Register your models here.
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Customer._meta.fields if field.name != 'user']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=[ field.name for field in Product._meta.fields]
    

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=[ field.name for field in Cart._meta.fields]
  

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=[ field.name for field in OrderPlaced ._meta.fields]


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')  # Columns to display in the admin list



