"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/httsp/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from store import views
from store.views import Home, Cart, Checkout, Search, Register, Login, UserOrders, logout, Product_details
from django.conf.urls.static import static

urlpatterns = [
    ## Django Built-in Admin Panel
    path('adminpanel/', admin.site.urls),
    ## Home Page View
    path('',Home.as_view(), name="home"),
    
    ## Producr Details Route
    
    path('products/<slug:slug>/', Product_details.as_view(), name="Product_details"),
    ## Cart View


    path('cart/', Cart.as_view(), name="cart"),

    ## Checkout View FOr Customers
    path('checkout/', Checkout.as_view(), name="checkout"),


    ## Searc Form Functions to search by products
    path('search_by_product/', Search.as_view(), name="search_by"),

    ## For Registering, Login and Logout 
    path('register/', Register.as_view(), name="register"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', views.logout, name="logout"),

    ## Showing Customers Orders By their own Id

    path('user_orders/', UserOrders.as_view(), name="user_orders"), 
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)