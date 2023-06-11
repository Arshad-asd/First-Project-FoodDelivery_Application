from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'), max_length=30, blank=True)
    mobile = PhoneNumberField(_('mobile number'), blank=True, null=True)
    otp = models.CharField(_('OTP'), max_length=6, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
       return self.email
    

class Product(models.Model):
    Product_name = models.CharField(max_length=255)
    description = models.TextField()
    Product_Image = models.ImageField(upload_to='product_images')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.Product_name

class ProductSize(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    offer_price = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    Quantity = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.size

class Category(models.Model):
    categoryes = models.CharField(max_length=50)

    def __str__(self):
        return self


class ProfileAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=100)
    phone_number = PhoneNumberField(_('mobile number'), blank=True, null=True)
    street = models.CharField(_('street'), max_length=100)
    city = models.CharField(_('city'), max_length=100)
    state = models.CharField(_('state'), max_length=100)
    country = models.CharField(_('country'), max_length=100)
    postal_code = models.CharField(_('postal code'), max_length=10)
    def __str__(self):
        return f"{self.user.email}'s Address"


class ProfilePic(models.Model):
     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
     profile_pic = models.ImageField(_('profile picture'), upload_to='profile_pics/')
     def __str__(self):
        return f"{self.user.email}'s Address"

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField('Product', through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_price(self):
        return sum(item.get_subtotal() for item in self.cart_items.all())
    def get_total_quantity(self):
        return sum(item.quantity for item in self.cart_items.all())


class CartItem(models.Model):
    user= models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    product_size = models.ForeignKey('ProductSize', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_active=models.BooleanField(default=True)

    def get_subtotal(self):
        return self.product_size.price * self.quantity


class Order(models.Model):
    ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Out for Shipping', 'Out for Shipping'),
    ('Confirmed', 'Confirmed'),
    ('Cancelled', 'Cancelled'),
    ('Out for Delivery', 'Out for Delivery'),
    ('Delivered', 'Delivered'),
   )

    PAYMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    )
    CHECKOUT_STATUS = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_no = models.AutoField(primary_key=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS)
    payment_method = models.CharField(max_length=50)
    checkout_status = models.CharField(max_length=50,choices=CHECKOUT_STATUS)
    to_address = models.ForeignKey('ProfileAddress', on_delete=models.CASCADE)
    total_mrp = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2)
    coupon_discount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)

class OrderItems(models.Model):
    order_no = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity= models.IntegerField(null=False)





