from django.http import request
from django.shortcuts import render, HttpResponse
from .models import *
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.



class Home(View):
    def get(self, request):
        products = Product.objects.all()
        cats = Category.objects.all()
        args = {'products':products, 'cats':cats}
        return render(self.request, 'Store/home.html', args)

    def post(self, request):
        product = request.POST.get('product')
        cart = request.session.get('cart')
        remove = request.POST.get('remove')

        if cart:
            quantity = cart.get(product)

            if quantity:
                if remove:
                    cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
            if cart[product] < 1:
                cart.pop(product)
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart

        return redirect('home')

class Product_details(View):
    def get(self, request, slug):
        pd = Product.objects.get(slug=slug)
        args = {}
        return render(self.request, 'Store/product_details.html', args)






class Cart(View):
    def map_function(self, product):
        cart = self.request.session.get('cart', None)
        product_id = str(product.id)

        if product_id in cart:
            if product.discount_price:
                return product.price * cart[product_id]
            else:

                return product.price * cart[product_id]



    def get(self, request):
        ids = list(request.session.get('cart').keys())
        cart_products = Product.get_products_id(ids)
        product_prices = list(map(self.map_function, cart_products))
        total = sum(product_prices)
        args = {'cart_products':cart_products, 'total':total}
        return render(self.request, 'Store/cart.html', args)


class Checkout(View):

    def get(self, request):
        return render(self.request, 'Store/checkout.html')

    def post(self, request):
        f_name = request.POST.get('f_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        method = request.POST.get('method')
        cart = request.session.get('cart')
        customer = request.session.get('customer')
        products = Product.get_products_id(list(cart.keys()))

        for product in products:
            # order = Order(customer=Customer(id=customer['id']), product=product, fname=fname,
            #               price=product.price, phone=phone, address=address, quantity=cart.get(str(product.id)))
            ## IF Product has Discount Price This method must be called

            if product.discount_price:
                order = Order(customer=Customer(id=customer['id']), product=product, fname=fname, price=product.discount_price, phone=phone, address=address, quantity=cart.get(str(product.id)))
            else:
                order = Order(customer=Customer(id=customer['id']), product=product, fname=fname,
                          price=product.price, phone=phone, address=address, quantity=cart.get(str(product.id)), city=city, method=method)



            order.save()

        request.session['cart'] = {}

        return redirect('user_orders')


class Search(View):
    def get(self, request):
        query = request.GET['query']
        products = Product.objects.filter(name__icontains=query)
        args = {'products': products}
        return render(self.request, 'Home/search.html', args)

class Register(View):
    def get(self, request):
        return render(request, 'Store/register.html')

    def post(self, request):
        # postData = request.POST
        # username = postData.get('username')
        # email = postData.get('email')
        # password = postData.get('password')
        # print(username, email, password)
        # customer = Customer(username=username,
        #                         email=email, password=password)
        # customer.password = make_password(customer.password)
        # customer.register()


        # return redirect('login')
        try:
            postData = request.POST
            username = postData.get('username')
            email = postData.get('email')
            password = postData.get('password')
            print(username, email, password)
            customer = Customer(username=username,
                                email=email, password=password)
            customer.password = make_password(customer.password)
            customer.register()


            return redirect('login')
        except:
            return HttpResponse("Email Or Phone Number Already Exists Please Try again")

class Login(View):
    def get(self, request):
        return render(request, 'Store/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer(email)
        error_message = None
        if customer:
            match = check_password(password, customer.password)
            if match:
                customer.__dict__.pop('_state')
                request.session['customer'] = customer.__dict__
                return redirect('home')
            else:
                error_message = 'Phone number or Password didnt match on our record'
        else:
            error_message = 'No Customer Found! Please Registrer First!'
        print(email, password)
        context = {'error_message': error_message}
        return render(request, 'Store/login.html', context)


def logout(request):
    request.session.clear()
    return redirect('home')



class UserOrders(View):
    def map_func(self, product):
        cart = self.request.session.get('cart', None)
        product_id = str(product.id)

        if product_id in cart:
            if not product.disc_price:

                return product.price * cart[product_id]
            else:
                return product.disc_price * cart[product_id]

    def get(self, request):
        customer = request.session.get('customer')
        user_orders = Order.get_orders_by_customer(customer)
        print(user_orders)
        args = {'user_orders': user_orders}
        return render(self.request, 'Home/all_orders.html', args)





## Payment View

def payment_view(request):



    params = {'USER' : 'xxxxxxxx', # Edit this to your API user name
        'PWD' : 'xxxxxxxx', # Edit this to your API password
        'SIGNATURE' : 'AFcWxV21C7fd0v3bYYYRCpSSRl31A0ltbCXAvF44j6B.kUqG3MePFr40',
        'METHOD':'SetExpressCheckout',
        'VERSION':86,
        'PAYMENTREQUEST_0_PAYMENTACTION':'SALE',     # type of payment
        'PAYMENTREQUEST_0_AMT':50,              # amount of transaction
        'PAYMENTREQUEST_0_CURRENCYCODE':'USD',
        'cancelUrl':"xxxxxxxxxxxxx",    #For use if the consumer decides not to proceed with payment
        'returnUrl':"xxxxxxxxxxxx"  #For use if the consumer proceeds with payment}
    }


    params_string = urllib.urlencode(params)
    response = urllib.urlopen('https://api-3t.sandbox.paypal.com/nvp', params_string).read() #gets the response and parse it.
    response_dict = parse_qs(response)
    response_token = response_dict['TOKEN'][0]
    rurl = PAYPAL_URL+response_token #gather the response token and redirect to paypal to authorize the payment
    return HttpResponseRedirect(rurl)
    # return render(request, 'Store/paypal.html', params)


def razor_pay(request):
    if request.method == 'POST':
        amount = 50000
        order_currency = 'RM'
        client = razorpay.Client(
            auth=('rzp_test_NJZIKFByHgvrqm', 'JEHpMASALEZQh7o4dVqoJjKy')
        )
        payment = client.order.create({'amount':amount, 'currency':'RM', 'payment_capture':1})
    return render(request, 'Store/razor_pay.html')

