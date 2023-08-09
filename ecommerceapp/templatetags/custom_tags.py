from django import template
from ecommerceapp.models import *
register = template.Library()

@register.filter()
def applydiscount(pid):
    data = Product.objects.get(id=pid)
    # price = int(data.price) * (100 - int(data.discount))/100
    print(data.price, data.discount)
    price = int(data.price)-(int(data.price)*int(data.discount)/100)
    return price

@register.filter()
def productimage(pid):
    data = Product.objects.get(id=pid)
    return data.image.url

@register.filter()
def productname(pid):
    data = Product.objects.get(id=pid)
    return data.name

@register.filter()
def productprice(pid):
    data = Product.objects.get(id=pid)
    return data.price

@register.filter()
def productdiscount(pid):
    data = Product.objects.get(id=pid)
    return data.discount

@register.simple_tag()
def producttotalprice(pid, qty):
    data = Product.objects.get(id=pid)
    price = int(data.price)-(int(data.price)*int(data.discount)/100)
    return ("%.2f" % (int(qty) * int(price)))