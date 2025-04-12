from django.db import models
from Authentication.models import User
from django_ckeditor_5.fields import CKEditor5Field
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator


# Create your models here.

DISTRICT_CHOICES = [
    ('Bhojpur', 'Bhojpur'),
    ('Dhankuta', 'Dhankuta'),
    ('Ilam', 'Ilam'),
    ('Jhapa', 'Jhapa'),
    ('Khotang', 'Khotang'),
    ('Morang', 'Morang'),
    ('Okhaldhunga', 'Okhaldhunga'),
    ('Panchthar', 'Panchthar'),
    ('Sankhuwasabha', 'Sankhuwasabha'),
    ('Solukhumbu', 'Solukhumbu'),
    ('Sunsari', 'Sunsari'),
    ('Taplejung', 'Taplejung'),
    ('Terhathum', 'Terhathum'),
    ('Udayapur', 'Udayapur'),
    ('Bara', 'Bara'),
    ('Dhanusha', 'Dhanusha'),
    ('Mahottari', 'Mahottari'),
    ('Parsa', 'Parsa'),
    ('Rautahat', 'Rautahat'),
    ('Saptari', 'Saptari'),
    ('Sarlahi', 'Sarlahi'),
    ('Siraha', 'Siraha'),
    ('Bhaktapur', 'Bhaktapur'),
    ('Chitwan', 'Chitwan'),
    ('Dhading', 'Dhading'),
    ('Dolakha', 'Dolakha'),
    ('Kathmandu', 'Kathmandu'),
    ('Kavrepalanchok', 'Kavrepalanchok'),
    ('Lalitpur', 'Lalitpur'),
    ('Makwanpur', 'Makwanpur'),
    ('Nuwakot', 'Nuwakot'),
    ('Ramechhap', 'Ramechhap'),
    ('Rasuwa', 'Rasuwa'),
    ('Sindhuli', 'Sindhuli'),
    ('Sindhupalchok', 'Sindhupalchok'),
    ('Baglung', 'Baglung'),
    ('Gorkha', 'Gorkha'),
    ('Kaski', 'Kaski'),
    ('Lamjung', 'Lamjung'),
    ('Manang', 'Manang'),
    ('Mustang', 'Mustang'),
    ('Myagdi', 'Myagdi'),
    ('Nawalpur', 'Nawalpur'),
    ('Parbat', 'Parbat'),
    ('Syangja', 'Syangja'),
    ('Tanahun', 'Tanahun'),
    ('Arghakhanchi', 'Arghakhanchi'),
    ('Banke', 'Banke'),
    ('Bardiya', 'Bardiya'),
    ('Dang', 'Dang'),
    ('Gulmi', 'Gulmi'),
    ('Kapilvastu', 'Kapilvastu'),
    ('Parasi', 'Parasi'),
    ('Palpa', 'Palpa'),
    ('Pyuthan', 'Pyuthan'),
    ('Rolpa', 'Rolpa'),
    ('Rukum East', 'Rukum East'),
    ('Rupandehi', 'Rupandehi'),
    ('Dailekh', 'Dailekh'),
    ('Dolpa', 'Dolpa'),
    ('Humla', 'Humla'),
    ('Jajarkot', 'Jajarkot'),
    ('Jumla', 'Jumla'),
    ('Kalikot', 'Kalikot'),
    ('Mugu', 'Mugu'),
    ('Rukum West', 'Rukum West'),
    ('Salyan', 'Salyan'),
    ('Surkhet', 'Surkhet'),
    ('Achham', 'Achham'),
    ('Baitadi', 'Baitadi'),
    ('Bajhang', 'Bajhang'),
    ('Bajura', 'Bajura'),
    ('Dadeldhura', 'Dadeldhura'),
    ('Darchula', 'Darchula'),
    ('Doti', 'Doti'),
    ('Kailali', 'Kailali'),
    ('Kanchanpur', 'Kanchanpur')
]

STATE_CHOICES = [
    ('Province 1', 'Province 1'),
    ('Madhesh Province', 'Madhesh Province'),
    ('Bagmati Province', 'Bagmati Province'),
    ('Gandaki Province', 'Gandaki Province'),
    ('Lumbini Province', 'Lumbini Province'),
    ('Karnali Province', 'Karnali Province'),
    ('Sudurpashchim Province', 'Sudurpashchim Province')
]
GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'other')
]


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='AvatarImages/', blank=True, null=True)

    fname = models.CharField(max_length=200)
    mname = models.CharField(max_length=200, blank=True)
    lname = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=10, unique=True, validators=[RegexValidator(
        r'^\d{10}$', message="Phone number must be 10 digits")])
    city = models.CharField(max_length=50)
    state = models.CharField(choices=STATE_CHOICES, max_length=50)
    district = models.CharField(choices=DISTRICT_CHOICES, max_length=100)
    gender = models.CharField(choices=GENDER_CHOICES,
                              max_length=10, default='Male')
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


CATEGORY_CHOICES = [
    ('Vegetables', 'Fresh Vegetables'),
    ('Fruits', 'Fresh Fruits'),
    ('DairyBakery', 'Dairy & Bakery Products'),
    ('Proteins', 'Proteins (Eggs, Meat, Fish, Plant-based)'),
    ('Beverages', 'Beverages (Tea, Coffee, Juices, Soft Drinks, Hard Drinks)'),
    ('PicklesJams', 'Pickles, Jams & Spreads'),
    ('InstantFoods', 'Instant & Ready-to-Eat Foods'),
    ('Grocery', 'Staples (rice,lentil,flour,grains) Frozen Foods & Ready-to-Cook'),
    ('Banner', 'Banner'),
    ('OffSeasonal', 'OffSeasonal'),
    ('OnSeasonal', 'OnSeasonal')

]


class Product(models.Model):
    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, default='Gauley')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    description = CKEditor5Field(config_name='extends')
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    discount_percent = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    weight = models.CharField(max_length=50, null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)

    first_product_image = models.ImageField(upload_to='ProductImg/')
    second_product_image = models.ImageField(
        upload_to='ProductImg/', null=True, blank=True)
    third_product_image = models.ImageField(
        upload_to='ProductImg/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f" {self.title} {str(self.id)}"



class Contact(models.Model):
    full_name = models.CharField(max_length=200)
    gmail = models.EmailField()
    phone_number = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return f"Contact from {self.full_name}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.product.title}"


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
    ('Pending', 'Pending'),
)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='Pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Amount field to store the total cost

    @property
    def total_cost(self):
        # This property will still calculate the total cost dynamically when accessed, if needed.
        return self.quantity * self.product.discount_price

    def save(self, *args, **kwargs):
        # Automatically update the amount before saving the order
        self.amount = self.quantity * self.product.discount_price
        super(OrderPlaced, self).save(*args, **kwargs)  # Call the parent class's save method