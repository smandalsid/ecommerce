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
    if not request.user.is_staff:
        return redirect("admin_login")
    category=Category.objects.all()
    if not request.user.is_staff:
        return redirect("admin_login")
    # if len(category)==0:
    #     return render(request, "add_category.html")
    # else:
    return render(request, "view_category.html", locals())

def edit_category(request, pid):
    if not request.user.is_staff:
        return redirect("admin_login")
    category = Category.objects.get(id=pid)
    if request.method == "POST":
        name = request.POST['name']
        category.name = name
        category.save()
        messages.success(request, "Category updated")
        return redirect('view_category')
    return render(request, 'edit_category.html', locals())

def delete_category(request, pid):
    if not request.user.is_staff:
        return redirect("admin_login")
    category = Category.objects.get(id=pid)
    category.delete()
    messages.success(request, "Category deleted")
    return redirect('view_category')

def add_product(request):
    if not request.user.is_staff:
        return redirect("admin_login")
    category=Category.objects.all()
    if request.method=="POST":
        name=request.POST["name"]
        price=request.POST["price"]
        category=request.POST["category"]
        discount=request.POST["discount"]
        description=request.POST["description"]
        image=request.FILES["image"]
        catobj = Category.objects.get(id=category)
        p=Product.objects.create(name=name, price=price, discount=discount, category=catobj, description=description, image=image)
        Carousel.objects.create(product=p)
        messages.success(request, "Product added")
    return render(request, "add_product.html", locals())

def view_products(request):
    if not request.user.is_staff:
        return redirect("admin_login")
    products=Product.objects.all()
    return render(request, "view_products.html", locals())

def edit_product(request, pid):
    if not request.user.is_staff:
        return redirect("admin_login")
    categories=Category.objects.all()
    product = Product.objects.get(id=pid)
    if request.method=="POST":
        name=request.POST["name"]
        price=request.POST["price"]
        category=request.POST["category"]
        cat=Category.objects.get(id=category)
        discount=request.POST["discount"]
        description=request.POST["description"]

        try:
            image=request.FILES["image"]
            product.image=image
            product.save()
        except:
            pass
        Product.objects.filter(id=pid).update(name=name, price=price, discount=discount, category=cat, description=description)
        messages.success(request, "Product Updated")
        return redirect("view_products")
    return render(request, "edit_product.html", locals())

def delete_product(request, pid):
    product=Product.objects.get(id=pid)
    product.delete()
    messages.success(request, "Product Deleted")
    return redirect("view_products")

def signup(request):
    if request.method=="POST":
        fname=request.POST["fname"]
        lname=request.POST["lname"]
        email=request.POST["email"]
        address=request.POST["address"]
        mobile=request.POST["mobile"]
        image=request.FILES["image"]
        password=request.POST["pass"]
        user=User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email, password=password)
        UserProfile.objects.create(user=user, mobile=mobile, address=address, image=image)
        messages.success(request, "Registration successful")
        return redirect('user_login')

    return render(request, "registrations.html", locals())

def user_login(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(username=username, password=password)
        if(user):
            login(request, user)
            messages.success(request, "Logged in Successully")
            return redirect('main')
        else:
            messages.success(request, "Failed to login")
    return render(request, "user_login.html", locals())

def edit_profile(request):
    user=UserProfile.objects.get(user=request.user)
    if request.method=="POST":
        fname=request.POST["fname"]
        lname=request.POST["lname"]
        email=request.POST["email"]
        mobile=request.POST["mobile"]
        address=request.POST["address"]
        try:
            image=request.FILES['image']
            user.image=image
            user.save()
        except:
            pass

        data=User.objects.filter(id=request.user.id).update(first_name=fname, last_name=lname)
        UserProfile.objects.filter(id=user.id).update(mobile=mobile, address=address)
        messages.success(request, "Profile Updated Successfully")
        return redirect('edit_profile')

    return render(request, "edit_profile.html", locals())

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged Out")
    return redirect('main')

def change_password(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            o=request.POST['curr']
            n=request.POST['new']
            r=request.POST['recon']
            user=authenticate(username=request.user.username, password=o)
            if user:
                if n==r:
                    user.set_password(n)
                    user.save()
                    messages.success(request, "Password changed successfully")
                    return redirect('main')
                else:
                    messages.success(request, "Passwords do not match")
            else:
                messages.success(request, "Invalid Password")
                return redirect('change_password')
    return render(request, 'change_password.html', locals())

def user_product(request, pid):
    if request.user.is_authenticated:
        if pid==0:
            product=Product.objects.all()
        else:
            category=Category.objects.get(id=pid)
            product=Product.objects.filter(category=category)
        allcategory=Category.objects.all()
    else:
        return redirect('user_login')

    return render(request, 'user_product_view.html', locals())

def admin_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged Out")
    return redirect('main')

def product_detail(request, pid):

    product=Product.objects.get(id=pid)
    actprice=int(product.price)-(int(product.discount)*int(product.price)/100)
    latest_product = Product.objects.filter().exclude(id=pid).order_by('-id')[:10]

    return render(request, "product_detail.html", locals())