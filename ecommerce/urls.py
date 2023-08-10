"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from ecommerceapp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', home, name="home"),
    path('index/', index, name="index"),
    path('about/', about, name="about"),
    path('', main, name="main"),
    path('admin_login/', admin_login, name="admin_login"),
    path('admin_home/', admin_home, name="admin_home"),
    path('admin_dashboard/', admin_dashboard, name="admin_dashboard"),
    path('add_category/', add_category, name="add_category"),
    path('view_category/', view_category, name="view_category"),
    path('edit_category/<int:pid>/', edit_category, name="edit_category"),
    path('delete_category/<int:pid>/', delete_category, name="delete_category"),
    path('add_product/', add_product, name="add_product"),
    path('view_products/', view_products, name="view_products"),
    path('edit_product/<int:pid>/', edit_product, name="edit_product"),
    path('delete_product/<int:pid>/', delete_product, name="delete_product"),
    path('signup/', signup, name="signup"),
    path('login/', user_login, name="user_login"),
    path('edit_profile/', edit_profile, name="edit_profile"),
    path('logout/', user_logout, name="logout"),
    path('change_password/', change_password, name="change_password"),
    path('user_product/<int:pid>', user_product, name="user_product"),
    path('admin_logout/', admin_logout, name="admin_logout"),
    path('product_detail/<int:pid>', product_detail, name="product_detail"),
    path('add_to_cart/<int:pid>/', add_to_cart, name="add_to_cart"),
    path('cart/', cart, name="cart"),
    path('incre/<int:pid>', incre, name="incre"),
    path('decre/<int:pid>', decre, name="decre"),
    path('deletecart/<int:pid>', deletecart, name="deletecart"),
    path('booking/', booking, name="booking"),
    path('my_order/', my_order, name="my_order"),
    path('user_order_track/<int:pid>', user_order_track, name="user_order_track"),
    path('cancel_order/<int:pid>', cancel_order, name="cancel_order"),
    path('return_order/<int:pid>', return_order, name="return_order"),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
