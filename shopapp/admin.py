from django.contrib import admin
from.models import Product,Order,OrderItem,Delivery,Category,Rate,Comment,Transaction,Profile
# Register your models here.

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Delivery)
admin.site.register(Category)
admin.site.register(Rate)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Transaction)