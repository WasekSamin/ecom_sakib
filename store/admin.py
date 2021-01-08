from django.contrib import admin
from store.models import Category, Brand, UOM, Product_Images, Product, Customer, City, Order, SubCategory, Currency 
# Register your models here.


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(UOM)
admin.site.register(Product_Images)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(City)
admin.site.register(Order)
admin.site.register(SubCategory)
admin.site.register(Currency)