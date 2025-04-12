from django.contrib import admin
from MainApp.models import Customer, Product, Cart, Contact, OrderPlaced, Wishlist

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Customer._meta.fields if field.name != 'user']
    search_fields = ['fname', 'lname', 'phone', 'city', 'district']

@admin.register(Contact)
class ContactrModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Contact._meta.fields]
    search_fields = ['full_name', 'gmail', 'phone_number', 'subject']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    search_fields = ['title', 'brand', 'category']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Cart._meta.fields]
    search_fields = ['user__email', 'product__title']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderPlaced._meta.fields]
    search_fields = ['user__email', 'product__title', 'status']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    search_fields = ['user__email', 'product__title']
