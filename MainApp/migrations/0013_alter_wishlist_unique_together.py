# Generated by Django 4.2.19 on 2025-03-06 11:06

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MainApp', '0012_remove_orderplaced_delivery_address_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='wishlist',
            unique_together={('user', 'product')},
        ),
    ]
