from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(myuser)
admin.site.register(Seller)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Categories)
admin.site.register(SubCategories)
admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Payment)