from django.db import models

# Create your models here.


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
    price = models.IntegerField(null=True)
    discount_price = models.IntegerField(null=True, blank=True)
    size = models.ManyToManyField(ProductSizes, blank=True)
    height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    color = models.ManyToManyField(ProductColors, blank=True)
    stock = models.BooleanField()
    SKU = models.CharField(max_length=150)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    # @staticmethod
    # def discount_precent():




    def __str__(self):
        return self.name


    def get_products_id(ids):
        return Product.objects.filter(id__in=ids)

class Customer(models.Model):
    username = models.CharField(max_length=155)
    # first_name = models.CharField(max_length=10)
    # last_name = models.CharField(max_length=10)
    email = models.CharField(max_length=155)
    password = models.CharField(max_length=155)


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
    quantity = models.IntegerField(default=1, null=True)
    invoice = models.AutoField(primary_key=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer")
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=150)
    price = models.IntegerField(null=True, blank=True)
    disc_price = models.IntegerField(null=True, blank=True)
    f_name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, related_name="city")
    method = models.ForeignKey(DeliveryMethod, on_delete=models.CASCADE, null=True, blank=True, related_name="method")
    order_status = models.CharField(null=True, blank=True, choices=STATUS, default="PENDING", max_length=155)
    total = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.disc_price:
            self.total = self.disc_price * self.quantity
        else:
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
        return Order.objects.filter(customer=customer['id'])


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