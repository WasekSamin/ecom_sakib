from django import template
from django.http import HttpResponse

register = template.Library()

@register.filter(name='in_cart')
def in_cart(product, cart):
	keys = cart.keys()
	for id in keys:
		if int(id) == product.id:
			return True
	return False

@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
	keys = cart.keys()
	quantity = 0

	for i in keys:
		if int(i) == product.id:
			quantity = cart.get(i)
		else:
			continue

	return quantity

# @register.filter(name='get_uom')
# def get_uom(product,cart):
#     if product.uom:
#         return HttpResponse("UOM ase")



@register.filter(name='cart_total')
def cart_total(product, cart):
    if product.discount_price:
        return product.discount_price * cart_quantity(product, cart)
    else:

	    return product.price * cart_quantity(product, cart)





@register.filter(name='get_total_cart_total')
def get_total_cart_total(products, cart):
	total = 0
	for p in products:
		total += cart_total(p, cart)
	return total









@register.filter(name="total_in_order")
def total_in_order(number, number1):
	return number * number1