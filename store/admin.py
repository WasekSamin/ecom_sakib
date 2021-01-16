from django.contrib import admin
from store.models import Category, Brand, UOM, ProductImages, Product, Customer, City, Order, SubCategory, Currency, DeliveryMethod, ProductColors, ProductSizes
# Register your models here.


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(UOM)
admin.site.register(ProductImages)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(City)
# admin.site.register(Order)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["customer", "product", "quantity", "price", "total", "phone", "address", "city", "method", "f_name", "invoice", "disc_price", "order_status"]
admin.site.register(SubCategory)
admin.site.register(Currency)
admin.site.register(DeliveryMethod)
admin.site.register(ProductColors)
admin.site.register(ProductSizes)