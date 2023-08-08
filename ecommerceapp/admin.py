from django.contrib import admin
from ecommerceapp.models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Carousel)
admin.site.register(UserProfile)
admin.site.register(Cart)