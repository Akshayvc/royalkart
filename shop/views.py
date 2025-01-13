from django.shortcuts import render, redirect
from .models import Product, Contact, Orders, OrderUpdate, Category, Supplier, Registration
from math import ceil
import json
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django import forms
from shop.forms import UserForm, UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.contrib import messages
# Create your views here.
from django.http import *
import requests

def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    data = Product.objects.values('category_id').distinct()
    for i in data:
        a = i['category_id']
        data1 = Product.objects.filter(category_id=i['category_id']).count()
        for o in cats:
            for j in catprods:
                data11 = Product.objects.filter(id=j['id'],category=a).values('count')
                for y in data11:
                    p = y['count']
                    r = p / data1
                    if r > 5:
                        r = r * 5 / data1
                    Product.objects.filter(id=j['id']).update(rate=r)
    edit = Supplier.objects.all()
    edit2 = Category.objects.all()
    params = {'allProds': allProds, 'edit':edit, 'edit2':edit2} 
    return render(request, 'shop/index.html', params)

def search(request):
    edit = Supplier.objects.all()
    edit2 = Category.objects.all()

    if request.method == 'POST':
        srch = request.POST['srh']

        if srch:
            match = Product.objects.filter(Q(product_name__icontains=srch)|Q(desc__icontains=srch))

            if match:
                return render(request, 'shop/search.html', {'sr':match, 'edit':edit})
            else:
                messages.error(request, 'no result found')
        else:
            return HttpResponseRedirect('/search/')

    return render(request, 'shop/search.html', {'edit':edit,'edit2':edit2})

def about(request):
    edit = Supplier.objects.all()
    edit2 = Category.objects.all()
    return render(request, 'shop/about.html',{'edit':edit,'edit2':edit2})

def contact(request):
    edit = Supplier.objects.all()
    edit2 = Category.objects.all()
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'shop/contact.html', {'edit':edit,'edit2':edit2})

def tracker(request):
    #fetch the supplier details
    edit2 = Category.objects.all()
    edit = Supplier.objects.all()
    #get the order id and email id entered by the user
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        #fetch the order details by filtering through email and order id
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            #if order found update the orderupdate table and append the description and time function
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            #if blank display no item found
            else:
                return HttpResponse('{"status":"noitem"}')
        #if orderid or email id doesn't match display error message stating orderid or emailid are invalid
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    #return the respective ordered details
    return render(request, 'shop/tracker.html', {'edit':edit,'edit2':edit2})
    
def productView(request, myid):
    pro2 = Product.objects.values('category')
    data2 = Product.objects.filter(id=myid).values('shop_name')
    data5 = Supplier.objects.values('shop_name','id')
    #fetch address using id
    for z in data2:
        q = z['shop_name']
        for t in data5:
            r = t['id']
            if q == r:
                data6 = Supplier.objects.filter(id=q)
    # Fetch the product using the product id
    product = Product.objects.filter(id=myid)
    w = product[0].product_name
    sv = Product.objects.filter(product_name=w)
    for i in sv:
        sv1 = Supplier.objects.filter(shop_name=i.shop_name).values('shop_name','address')
        print(sv1)
    #fetch the category id of the product using the product id
    data = Product.objects.filter(id=myid).values('category')
    for z in data:
        a = z['category']
        for x in pro2:
            #fetch all the categories and their id from Product table
            y = x['category']
            #compare the "a"(filter category id value) with the category id value in Product table
            if a == y:
                #if found fetch the respective product details of that category and return the values obtained
                data3 = Product.objects.filter(category = a)
    data4 = data3
    data7 = data6
    #counting the visit to a particular product
    data11 = Product.objects.filter(id=myid).values('count')
    for i in data11:
        p = i['count']
        p = p + 1
        Product.objects.filter(id=myid).update(count=p)
    data12 = Product.objects.filter(category=a).order_by('-count')
    edit2 = Category.objects.all()
    edit = Supplier.objects.all()
    return render(request, 'shop/prodView.html', {'product': product[0], 'data4':data4, 'data7':data7, 'data12':data12, 'edit':edit,'edit2':edit2, 'sv':sv, 'sv1':sv1})

def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('productname', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + \
            " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        shopname = request.POST.get('shopname', '')
        shop_id = Supplier.objects.filter(shop_name = shopname)
        sid = [i.id for i in shop_id]
        print(sid)
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, shop_name_id = sid[0])
        
        order.save()
        update = OrderUpdate(order_id=order.order_id,
                             update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            city = userObj['city']
            pin_code = userObj['pin_code'] 
            mobile = userObj['mobile']
            password =  userObj['password']
            cpassword = userObj['verify']                       
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                update = Registration(name=username,email=email,mobile="123",city=city,pincode=pin_code,username=mobile,password=password,confirm=cpassword)
                update.save()
                print(update)
                return HttpResponseRedirect('../user_login')
            else:
                return render(request, 'shop/verify.html')
                
    else:
        form = UserRegistrationForm()
    return render(request, 'shop/registration.html', {'form' : form})

def user_login(request):
    global username
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive")
        else:
            return render(request, 'shop/validate.html')
    else:
        return render(request, 'shop/login.html', {})
    
def profile(request):
    uname = username
    return render(request, 'shop/profile.html', {'uname': uname})

def basic(request):
    id = request.GET['id']
    data = Product.objects.filter(shop_name_id = id)
    edit = Supplier.objects.all()
    edit1 = Supplier.objects.filter(id=id)
    edit2 = Category.objects.all()
    return render(request, 'shop/filterdisplay.html', {'details': data, 'edit':edit, 'edit1':edit1, 'edit2':edit2})

def basics(request):
    edit2 = Category.objects.all()
    id = request.GET['cat']
    data = Product.objects.filter(category = id)
    edit = Supplier.objects.all()
    edit1 = Category.objects.filter(id=id)
    return render(request, 'shop/category.html', {'details': data, 'edit':edit, 'edit1':edit1, 'edit2':edit2})
