# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthenticationUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.IntegerField()
    is_staff = models.IntegerField()
    is_superuser = models.IntegerField()
    is_customer = models.IntegerField()
    is_seller = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'authentication_user'


class BlogArticle(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'blog_article'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthenticationUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class MainappCart(models.Model):
    id = models.BigAutoField(primary_key=True)
    quantity = models.PositiveIntegerField()
    added_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    product = models.ForeignKey('MainappProduct', models.DO_NOTHING)
    user = models.ForeignKey(AuthenticationUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'mainapp_cart'


class MainappCustomer(models.Model):
    id = models.BigAutoField(primary_key=True)
    fname = models.CharField(max_length=200)
    mname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(unique=True, max_length=10)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=100)
    user = models.ForeignKey(AuthenticationUser, models.DO_NOTHING)
    gender = models.CharField(max_length=10)
    avatar = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mainapp_customer'


class MainappOrderplaced(models.Model):
    id = models.BigAutoField(primary_key=True)
    quantity = models.PositiveIntegerField()
    ordered_date = models.DateTimeField()
    status = models.CharField(max_length=50)
    customer = models.ForeignKey(MainappCustomer, models.DO_NOTHING)
    product = models.ForeignKey('MainappProduct', models.DO_NOTHING)
    user = models.ForeignKey(AuthenticationUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'mainapp_orderplaced'


class MainappProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.TextField()
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    discount_percent = models.IntegerField()
    stock = models.PositiveIntegerField()
    is_available = models.IntegerField()
    weight = models.CharField(max_length=50, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    first_product_image = models.CharField(max_length=100)
    second_product_image = models.CharField(max_length=100, blank=True, null=True)
    third_product_image = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mainapp_product'


class MainappWishlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    added_at = models.DateTimeField()
    product = models.ForeignKey(MainappProduct, models.DO_NOTHING)
    user = models.ForeignKey(AuthenticationUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'mainapp_wishlist'
        unique_together = (('user', 'product'),)


class PaymentgatewayPayment(models.Model):
    id = models.BigAutoField(primary_key=True)
    payment_method = models.CharField(max_length=20)
    payment_status = models.CharField(max_length=20)
    payment_date = models.DateTimeField()
    transaction_id = models.CharField(unique=True, max_length=255, blank=True, null=True)
    order = models.OneToOneField(MainappOrderplaced, models.DO_NOTHING)
    invoice_no = models.CharField(unique=True, max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'paymentgateway_payment'


class RatingandreviewOverallreview(models.Model):
    id = models.BigAutoField(primary_key=True)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    user = models.ForeignKey(AuthenticationUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ratingandreview_overallreview'


class RatingandreviewProductreview(models.Model):
    id = models.BigAutoField(primary_key=True)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    product = models.ForeignKey(MainappProduct, models.DO_NOTHING)
    user = models.ForeignKey(AuthenticationUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ratingandreview_productreview'
