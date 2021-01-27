from django.db import models

from django.db.models.signals import pre_save
from .random_order_id_gen import random_id_generator
# Create your models here.

def unique_order_id_generator(instance, new_id=None):
    if new_id is not None:
        return new_id
    return random_id_generator(6)


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=200)
    cat_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

## Subcategory

class SubCategory(models.Model):
    sub_title = models.CharField(max_length=50)
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.sub_title



class Brand(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=200)
    brand_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

class UOM(models.Model):
    title = models.CharField(max_length=100)
    height = models.DecimalField(null=True, default=0, max_digits=10, decimal_places=2)
    width = models.DecimalField(null=True, default=0, max_digits=10, decimal_places=2)
    weight = models.DecimalField(null=True, default=0, max_digits=10, decimal_places=2)
    length = models.DecimalField(null=True, default=0, max_digits=10, decimal_places=2)
    quantity = models.IntegerField(null=True, default=1)

    def __str__(self):
        return self.title

class ProductImages(models.Model):
    multi_images = models.ImageField(upload_to='images/')

    def __str__(self):
        return str(self.multi_images)

class Currency(models.Model):
    curr_sign = models.CharField(max_length=10)

    def __str__(self):
        return self.curr_sign

class ProductColors(models.Model):
    cl_name = models.CharField(max_length=155)

    def __str__(self):
        return self.cl_name


class ProductSpces(models.Model):
    spec_title = models.CharField(max_length=155)

    def __str__(self):
        return self.spec_title


class ProductSizes(models.Model):
    SIZES = [
            ("S", "S"),
            ("M", "M"),
            ("L", "L"),
            ("XL", "XL"),
            ("XXL", "XXL")
        ]
    size_name = models.CharField(max_length=50, null=True, blank=True, choices=SIZES)

    def __str__(self):
        return self.size_name


class Product(models.Model):
    name = models.CharField(max_length=100)

    slug = models.CharField(max_length=200)
    product_main_image = models.ImageField(upload_to="images/", null=True, blank=True)
    product_other_images = models.ManyToManyField(ProductImages, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    price = models.IntegerField(null=True, default=0)
    discount_price = models.IntegerField(null=True, blank=True, default=0)
    discount_percentage = models.IntegerField(null=True, blank=True, default=0)
    size = models.ManyToManyField(ProductSizes, blank=True)
    # height = models.IntegerField(null=True, blank=True)
    # weight = models.IntegerField(null=True, blank=True)
    # length = models.IntegerField(null=True, blank=True)
    color = models.ManyToManyField(ProductColors, blank=True)
    spec = models.ManyToManyField(ProductSpces, blank=True)
    uoms = models.ManyToManyField(UOM)
    stock = models.BooleanField()
    SKU = models.CharField(max_length=150)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


    # def save(self, *args, **kwargs):
    #     if uoms == 'CTN':
    #         self.price = self.price * 10
    #         return self.price
    #     else:
    #         self.price = self.price * 1
    #         return self.price
    #     super().save(*args, **kwargs)
    def get_products_id(ids):
        return Product.objects.filter(id__in=ids)


# Discount precentage create signal
def discount_precentage_receiver(sender, instance, *args, **kwargs):
    if not instance.discount_percentage and instance.discount_price and instance.price:
        if instance.discount_price > 0:
            instance.discount_percentage = 100 - abs((instance.discount_price / instance.price) * 100)
        else:
            instance.discount_percentage = 0
        instance.save()

pre_save.connect(discount_precentage_receiver, sender=Product)


# Discount precentage remover signal
def discount_precentage_remover(sender, instance, *args, **kwargs):
    if instance.discount_percentage and not instance.discount_price:
        instance.discount_percentage = 0
        instance.save()

pre_save.connect(discount_precentage_remover, sender=Product)


class Customer(models.Model):
    username = models.CharField(max_length=155, null=True)
    # first_name = models.CharField(max_length=10)
    # last_name = models.CharField(max_length=10)
    email = models.CharField(max_length=155, unique=True, null=True)
    password = models.CharField(max_length=155, null=True)


    def __str__(self):
        return self.username

    def register(self):
        self.save()
    def get_customer(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False;

class City(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name


class DeliveryMethod(models.Model):
    title = models.CharField(max_length=155)

    def __str__(self):
        return self.title

class OrderStatus(models.Model):
    st_title = models.CharField(max_length=155, default="Pending")


    def __str__(self):
        return self.st_title



class Order(models.Model):

    STATUS = (
        ("PENDING", "PENDING"),
        ("PICKED", "PICKED"),
        ("DELIVERED", "DELIVERED")
        )


    product = models.ForeignKey(
        Product, null=True, on_delete=models.CASCADE, related_name="product")
    quantity = models.IntegerField(default=0, null=True)
    invoice = models.CharField(max_length=10, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer")
    phone = models.CharField(max_length=12, null=True)
    address = models.CharField(max_length=150, null=True)
    price = models.IntegerField(null=True, blank=True)
    f_name = models.CharField(max_length=100, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, related_name="city")
    method = models.ForeignKey(DeliveryMethod, on_delete=models.CASCADE, null=True, blank=True, related_name="method")
    order_status = models.CharField(null=True, blank=True, choices=STATUS, default="PENDING", max_length=155)
    total = models.IntegerField(default=0, null=True)

    def save(self, *args, **kwargs):
        if self.price:
            self.total = self.price * self.quantity
        super().save(*args, **kwargs)

    @staticmethod
    def get_total(self):
        return Order.objects.filter(total=self.total)

    @staticmethod
    def get_all_orders(self):
        return Order.objects.all()

    @staticmethod
    def placeOrder(self):
        return self.save()

    @staticmethod
    def get_orders_by_customer(customer):
        if customer:
            return Order.objects.filter(customer=customer['id'])

def pre_save_order_id_recciever(sender, instance, *args, **kwargs):
    if not instance.invoice:
        instance.invoice = unique_order_id_generator(instance)

pre_save.connect(pre_save_order_id_recciever, sender=Order)


class Slider(models.Model):
    title = models.CharField(max_length=100, null=True)
    img = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.title


class Bundle(models.Model):
    title = models.CharField(max_length=100, blank=True)
    bundle_img = models.ImageField(upload_to='images/', blank=True)


class OrderManager(models.Model):
    user_name = models.CharField(max_length=100)
    user_pass = models.CharField(max_length=10)