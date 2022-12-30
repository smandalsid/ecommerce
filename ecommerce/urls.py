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
    path('', home, name="home"),
    path('index/', index, name="index"),
    path('about/', about, name="about"),
    path('main/', main, name="main"),
    path('admin_login/', admin_login, name="admin_login"),
    path('admin_home/', admin_home, name="admin_home"),
    path('admin_dashboard/', admin_dashboard, name="admin_dashboard"),
    path('add_category/', add_category, name="add_category"),
    path('view_category/', view_category, name="view_category"),
    path('edit_category/<int:pid>/', edit_category, name="edit_category"),
    path('delete_category/<int:pid>/', delete_category, name="delete_category"),
    path('add_product/', add_product, name="add_product"),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
