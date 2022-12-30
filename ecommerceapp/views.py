from django.shortcuts import render, redirect
from ecommerceapp.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'navbar.html')

def about(request):
    return render(request, "about.html")

def main(request):
    data=Carousel.objects.all()
    d={'data':data}
    return render(request, "index.html", d)

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("admin_dashboard")
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username, password=password)
        try:
            if user.is_staff==True:
                login(request, user)
                messages.success(request, "Login success")
                return redirect('admin_dashboard')
            else:
                messages.success(request, "Invalid Credentials")
        except:
            messages.success(request, "Invalid Credentials")
    return render(request, "admin_login.html")

def admin_home(request):
    return render(request, "admin_base.html")

def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect("admin_login")
    return render(request, "admin_dashboard.html")

def add_category(request):
    if not request.user.is_staff:
        return redirect("admin_login")
    msg=None
    if request.method=="POST":
        name=request.POST['name']
        Category.objects.create(name=name)
        messages.success(request, "Category added")
        return redirect('view_category')

    return render(request, "add_category.html", locals())

def view_category(request):
    category=Category.objects.all()
    if not request.user.is_staff:
        return redirect("admin_login")
    # if len(category)==0:
    #     return render(request, "add_category.html")
    # else:
    return render(request, "view_category.html", locals())

def edit_category(request, pid):
    category = Category.objects.get(id=pid)
    if request.method == "POST":
        name = request.POST['name']
        category.name = name
        category.save()
        messages.success(request, "Category updated")
        return redirect('view_category')
    return render(request, 'edit_category.html', locals())

def delete_category(request, pid):
    category = Category.objects.get(id=pid)
    category.delete()
    messages.success(request, "Category deleted")
    return redirect('view_category')

def add_product(request):
    if not request.user.is_staff:
        return redirect("admin_login")
    return render(request, "add_product.html")