from email.mime import image
from email.policy import default
from random import choices
from django.db import models


# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey
from .managers import CustomUserManager
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django_countries.fields import CountryField
from taggit.managers import TaggableManager

class myuser(AbstractBaseUser, PermissionsMixin):
    email= models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_customer = models.BooleanField(default= False)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'

class City(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length= 100)

    def __str__(self):
        return f'{self.name}'

Gender = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]

class Customer(models.Model):
    user = models.OneToOneField(myuser, on_delete=models.CASCADE)
    gender = models.CharField(max_length= 100, choices=Gender, null=False, blank= False)
    birth_date = models.DateField(null=False, blank= False)
    phone_number = models.CharField(max_length= 100, null=False, blank= False)
    profile_image =models.ImageField(upload_to ='profile_image/')
    delivery_address = models.CharField(max_length=100, null =False, blank = False)
    region = models.ForeignKey(Region, on_delete =models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)


BusinessModel =[
    ('Individual', 'Individual'),
    ('Company', 'Company'),
    ('Registered Business Name', 'Registered Business Name'),
]

class Seller(models.Model):
    user = models.OneToOneField(myuser, on_delete= models.CASCADE)
    shop_name = models.CharField(max_length= 100)
    business_type = models.CharField(max_length= 100, choices= BusinessModel, null=False,blank=False, help_text='Please select if you are an individual or Business Entity/Company')
    phone_number = models.CharField(max_length=20, null =False, blank = False)
    address = models.CharField(max_length=100, null =False, blank = False)
    city = models.ForeignKey(City, on_delete= models.CASCADE)
    bank_name = models.CharField(max_length = 100)
    account_name = models.CharField(max_length = 100)
    account_number = models.CharField(max_length = 11,null=True)

    def __str__(self):
        return f'{self.shop_name}'

class Categories(models.Model):
    title = models.CharField(max_length =100)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name_plural = 'Categories'

class SubCategories(models.Model):
    category = models.ForeignKey(Categories, on_delete= models.CASCADE)
    title = models.CharField(max_length= 100)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name_plural = 'SubCategories'

class Product(models.Model):
    category = models.ForeignKey(Categories, on_delete = models.CASCADE)
    name = models.CharField(max_length =100)
    seller = models.ForeignKey(Seller, on_delete = models.CASCADE)
    description = RichTextUploadingField()
    brand = models.CharField(max_length = 100, help_text= 'Brand of the product', null=True, blank =True)
    main_image = models.ImageField(upload_to='Product/Main-image/')
    image2= models.ImageField(upload_to='Product/Main-image/')
    image3 =models.ImageField(upload_to='Product/Main-image/', null=True, blank =True)
    image4= models.ImageField(upload_to='Product/Main-image/', null=True, blank =True)
    created_date = models.DateTimeField(auto_now_add = True)
    price = models.DecimalField(max_digits=10, decimal_places = 2)
    discount_price = models.DecimalField(max_digits=10, decimal_places = 2)
    available = models.BooleanField(default =True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product", kwargs={"pk": self.pk})

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={
            'pk':self.pk
        })
    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'pk':self.pk
        })

class OrderProduct(models.Model):
    user = models.ForeignKey(myuser, on_delete=models.CASCADE)
    ordered= models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_total_item_price(self):
        return self.quantity * self.product.price

    def get_discount_item_price(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        return self.get_discount_item_price() - self.get_discount_item_price()

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_discount_item_price()

        return self.get_total_item_price()

DeliveryMethod= (
    ('D', 'Door Delivery'),
    ('P', 'Pickup Station')

)

class Order(models.Model):
    user = models.ForeignKey(myuser, on_delete=models.CASCADE)
    product = models.ManyToManyField(OrderProduct)
    start_date= models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    delivery_method = models.CharField(max_length=100, choices=DeliveryMethod, null=True, blank=True)

    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True
    )    

    def get_total_price(self):
        total = 0
        for order_item in self.product.all():
            total += order_item.get_final_price()

        return total

class Payment(models.Model):
    user = models.ForeignKey(
        myuser, on_delete = models.SET_NULL, blank =True, null=True
    )
    amount= models.FloatField()
    timestamp= models.DateTimeField(auto_now_add=True)

