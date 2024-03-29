from django.shortcuts import render, redirect
from ecommerceapp.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import json
from django.conf import settings
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
# Create your views here.

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

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
    if not request.user.is_authenticated:
        return redirect('user_login')
    product=Product.objects.get(id=pid)
    actprice=int(product.price)-(int(product.discount)*int(product.price)/100)
    latest_product = Product.objects.filter().exclude(id=pid).order_by('-id')[:10]

    return render(request, "product_detail.html", locals())

def add_to_cart(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    myli={"objects":[]}
    try:
        cart=Cart.objects.get(user=request.user)
        myli=json.loads((str(cart.product)).replace("'", '"'))
        try:
            myli['objects'][0][str(pid)]=myli['objects'][0].get(str(pid), 0)+1
        except:
            myli['objects'].append({str(pid):1})
        cart.product=myli
        cart.save()
    except:
        myli['objects'].append({str(pid):1})
        cart=Cart.objects.create(user=request.user, product=myli)
    return redirect('cart')

def decre(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    cart=Cart.objects.get(user=request.user)
    myli=json.loads((str(cart.product)).replace("'", '"'))
    if myli['objects'][0][str(pid)]==1:
        del myli['objects'][0][str(pid)]
    else:
        myli['objects'][0][str(pid)]=myli['objects'][0].get(str(pid), 0)-1
    cart.product=myli
    cart.save()
    return redirect('cart')

def incre(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    cart=Cart.objects.get(user=request.user)
    myli=json.loads((str(cart.product)).replace("'", '"'))
    myli['objects'][0][str(pid)]=myli['objects'][0].get(str(pid), 0)+1
    cart.product=myli
    cart.save()
    return redirect('cart')

def cart(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    try:
        cart=Cart.objects.get(user=request.user)
        product=(cart.product).replace("'", '"')
        myli = json.loads(str(product))
        product = myli['objects'][0]
    except:
        product=[]
    lenpro=len(product)
    return render(request, 'cart.html', locals())

def deletecart(request, pid):
    cart=Cart.objects.get(user=request.user)
    product=(cart.product).replace("'", '"')
    myli=json.loads(str(product))

    del myli['objects'][0][str(pid)]
    cart.product=myli
    cart.save()
    messages.success(request, "Deleted Successfully")
    return redirect('cart')

def deletecart(request, pid):
    cart=Cart.objects.get(user=request.user)
    product=(cart.product).replace("'", '"')
    myli=json.loads(str(product))

    del myli['objects'][0][str(pid)]
    cart.product=myli
    cart.save()
    messages.success(request, "Deleted Successfully")
    return redirect('cart')

def booking(request):

    if not request.user.is_authenticated:
        return redirect('user_login')
    
    user=UserProfile.objects.get(user=request.user)
    cart=Cart.objects.get(user=request.user)
    total=0

    productid=(cart.product).replace("'", '"')
    productid=json.loads(str(productid))

    try:
        productid=productid['objects'][0]
    except:
        messages.success(request, "Cart is empty!!")
        return redirect('cart')
    for i, j in productid.items():
        product=Product.objects.get(id=i)
        total+=int(int(j)*(int(product.price)-(int(product.price)*int(product.discount)/100)))

    currency="INR"
    amount=total*100
    razorpay_order=razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
    razorpay_order_id=razorpay_order['id']
    callback_url='../payment_handler/'

    context={}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    
    # if request.method=="POST":
        # book=Booking.objects.create(user=request.user, product=cart.product, total=total)
        # cart.product={"objects":[]}
        # cart.save()
    #     messages.success(request, "Order placed successfully")
    #     return redirect('main')
    return render(request, "booking.html", locals())  

@csrf_exempt
def payment_handler(request):

    if not request.user.is_authenticated:
        return redirect('user_login')
    
    user=UserProfile.objects.get(user=request.user)
    cart=Cart.objects.get(user=request.user)
    total=0

    productid=(cart.product).replace("'", '"')
    productid=json.loads(str(productid))

    try:
        productid=productid['objects'][0]
    except:
        messages.success(request, "Cart is empty!!")
        return redirect('cart')
    for i, j in productid.items():
        product=Product.objects.get(id=i)
        total+=int(int(j)*(int(product.price)-(int(product.price)*int(product.discount)/100)))

    if request.method=="POST":
        try:
            payment_id=request.POST.get('razorpay_payment_id', '')
            razorpay_order_id=request.POST.get('razorpay_order_id', '')
            signature=request.POST.get('razorpay_signature', '')
            params_dict={
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id' : payment_id,
                'razorpay_signature': signature,
            }

            result=razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                amount=total*100
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    book=Booking.objects.create(user=request.user, product=cart.product, total=total, razorpay_order_id=razorpay_order_id, razorpay_payment_id=payment_id)
                    cart.product={"objects":[]}
                    cart.save()
                    messages.success(request, "Order placed successfully")
                    return redirect("my_order")
                except:
                    messages.success(request, "Error placing the order")
                    return redirect("cart")
            else:
                messages.success(request, "Error placing the order")
                return redirect("cart")
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()
    

def my_order(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    orders=Booking.objects.filter(user=request.user)
    return render(request, 'my_order.html', locals())

def user_order_track(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    try:
        order=Booking.objects.get(id=pid)
        if order.user!=request.user:
            messages.success(request, "WHAT DA DOG DOIN?")
            return redirect('main')
        status=int(order.status)
    except:
        messages.success(request, "WHAT DA DOG DOIN?")
        return redirect('main')
    return render(request, "user_order_track.html", locals())

def cancel_order(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    try:
        order=Booking.objects.get(id=pid)
        if order.user!=request.user:
            messages.success(request, "WHAT DA DOG DOIN?")
            return redirect('main')
        
        order.status=5
        order.save()
        messages.success(request, "Order cancelled successfully")
    except:
        messages.success(request, "WHAT DA DOG DOIN?")
        return redirect('main')
    return redirect('my_order')

def return_order(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    try:
        order=Booking.objects.get(id=pid)
        if order.user!=request.user:
            messages.success(request, "WHAT DA DOG DOIN?")
            return redirect('main')
        
        order.status=6
        order.save()
        messages.success(request, "Order return initiated")
    except:
        messages.success(request, "WHAT DA DOG DOIN?")
        return redirect('main')
    return redirect('my_order')

def feedback(request, pid):
    if not request.user.is_authenticated:
        return redirect('main')
    
    try:
        order=Booking.objects.get(id=pid)
        fbs=Feedback.objects.filter(order=order)
        user=UserProfile.objects.get(user=request.user)
        if request.user!=order.user:
            messages.success(request, "WHAT DA DOG DOIN?")
            return redirect('main')
        if request.method=="POST":
            sub=request.POST["subject"]
            msg=request.POST["feedback"]
            fb=Feedback.objects.create(user=request.user, order=order, subject=sub, feedback=msg)
            messages.success(request, "Feedback submitted")
            return redirect("my_order")
    except:
        messages.success(request, "WHAT DA DOG DOIN?")
        return redirect('main')
    return render(request, "feedback.html", locals())

def delete_feedback(request, pid):
    fb=Feedback.objects.get(id=pid)
    fb.delete()
    messages.success(request, "Feedback deleted")
    return redirect("my_order")

def order_details(request, pid):
    if not request.user.is_authenticated:
        return redirect('main')
    try:
        order=Booking.objects.get(id=pid)
        if request.user!=order.user:
            messages.success(request, "WHAT DA DOG DOIN?")
            return redirect("main")
        product=(order.product).replace("'", '"')
        myli = json.loads(str(product))
        product = myli['objects'][0]
    except:
        messages.success(request, "WHAT DA DOG DOIN?")
        return redirect("main")
    return render(request, "order_details.html", locals())

def manage_feedback(request):
    if not request.user.is_authenticated:
        messages.success(request, "WHAT DA DOG DOIN?")
        return redirect("admin_login")
    if request.user.is_staff==False:
        return redirect("admin_login")
    fbs=Feedback.objects.all()
    return render(request, "manage_feedback.html", locals())

def admin_delete_feedback(request, pid):
    if not request.user.is_authenticated:
        messages.success(request, "WHAT DA DOG DOIN?")
        return redirect("admin_login")
    if request.user.is_staff==False:
        return redirect("admin_login")
    try:
        fb=Feedback.objects.get(id=pid)
        fb.delete()
        messages.success(request, "Feedback deleted")
    except:
        messages.success(request, "Something went wrong")
    return redirect("manage_feedback")