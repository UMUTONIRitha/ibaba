from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from tinymce.models import HTMLField
import datetime as dt
from django.db.models import Q
import numpy as np
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128)
    second_name = models.CharField(max_length=128)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    my_location  = models.CharField(max_length=128)
    profile_pic = models.ImageField(upload_to='profile/', default='a.png')
    def __str__(self):
        return self.user.username

    @classmethod
    def search_by_profile(cls, username):
        certain_user = cls.objects.filter(user__username__icontains = username)
        return certain_user

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
         if created:
            Profile.objects.create(user=instance)
            instance.profile.save() 

    @classmethod
    def get_by_id(cls, id):
        profile = Profile.objects.get(user = id)
        return profile

    @classmethod
    def filter_by_id(cls, id):
        profile = Profile.objects.filter(user = id).first()
        return profile

class Category(models.Model):
    name = models.CharField(max_length =30)
    def __str__(self):
        return self.name 
    @classmethod
    def get_category(cls):
        categories = Category.objects.all()
        return categories   
    def save_category(self):
        self.save()
    def delete_category(self):
        self.delete() 

class Product(models.Model):
    name = models.CharField(max_length=250, blank=True)
    product_pic = models.ImageField(upload_to='products/')
    description = models.TextField(max_length=255)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ["-pk"]

    def avg_price(self):
        price_rates = list(map(lambda x: x.prices, self.project.all()))
        return np.mean(price_rates)

    def avg_quality(self):
        fresheness_rates = list(map(lambda x: x.qualities, self.project.all()))
        return np.mean(quality_rates)

    def avg_delivery(self):
        delivery_rates = list(map(lambda x: x.deliveries, self.project.all()))
        return np.mean(delivery_rates)  

    def save_product(self):
        self.save()
    def get_absolute_url(self):
        return f"/product/{self.id}"

    def delete_product(self):
        self.delete()
    @classmethod
    def search_by_name(cls,search_term):
        certain_user = cls.objects.filter(name__icontains = search_term)
        return certain_user
    def __str__(self):
        return self.name

    @classmethod
    def filter_by_category(cls, category):
        product = Product.objects.filter(category__name=category).all()
        return product

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)
    quantity = models.IntegerField(default=1)   

    def __str__(self):
        return self.product.name
    # def get_total_grocery_price(self):         
    #     return self.quantity * self.grocery.price           
    def get_final_price(self):
        return self.get_total_product_price

class Order(models.Model):
    ref_code = models.CharField(max_length=15)
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ForeignKey(OrderItem, blank=True, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now=True)
    sub_total_amount = models.DecimalField(default=1, blank=True,  decimal_places=2, max_digits=19)

    def get_cart_items(self):
        return self.items.all()

    def delete_cat(self):
        self.delete()   

    def get_cart_total(self):
        # total = 0
        # for OrderItem in self.items.all():
        #     total += OrderItem.get_final_price()
        # return total       
        return sum([item.items.product.subtotal for item in self.items.all()])


    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.ref_code)

class Transaction(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    token = models.CharField(max_length=120)
    order_id = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    success = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.order_id
    class Meta:
        ordering = ['-timestamp']

class Comment(models.Model):
    comment = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.comment
    class Meta:
        ordering = ["-pk"]    

class Rate(models.Model):
    rating = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='project', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='rate')
    prices = models.IntegerField(choices=rating, default=0, blank=True)
    qualities = models.IntegerField(choices=rating,default=0, blank=True)
    deliveries = models.IntegerField(choices=rating,default=0, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def save_rate(self):
        self.save()
    class Meta:
        ordering = ["-pk"]   

class Delivery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='deliver')
    location  = models.CharField(max_length=128)
    phone = PhoneField(blank=True, help_text='Contact phone number')

    # email = models.EmailField(db.String(255), unique = True, index = True)
    # cc_expiry = CardExpiryField('expiration date')
    # cc_code = SecurityCodeField('security code')

    def save_deliver(self):
        self.save()
    class Meta:
        ordering = ["-pk"] 
