from django.contrib import admin
from PaymentGateway.models import Payment

@admin.register(Payment)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Payment._meta.fields if field.name != 'user']
