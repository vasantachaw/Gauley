from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from Authentication.models import User
# Register your models here.

class UserModelAdmin(UserAdmin):
    model = User
    list_display = ['id', 'email', 'name', 'is_active', 'is_staff',
                    'is_customer', 'is_superuser']  # Customize as per your model
    search_fields = ['email']
    ordering = ['email', 'id']
    list_filter = ['is_superuser']
    filter_horizontal = []
    # Custom fieldsets if your model has different fields
    fieldsets = [
        ('User Credentials',{'fields':['email','password']}),
        ('Personal Info', {'fields': ('name', 'city')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'is_customer', 'is_seller')}),
       
    ]

    add_fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         )
    ]
admin.site.register(User, UserModelAdmin)