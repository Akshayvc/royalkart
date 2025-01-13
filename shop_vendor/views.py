from django.shortcuts import render, redirect, render_to_response
from .models import Supplier
from shop.models import Product,Category,Orders,Contact
from django.contrib.auth import login, logout, authenticate
from django.http import *
from django.db.models import Q
from shop.forms import UserForm, UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.views import checkout
import requests

# Create your views here.
def index(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        global srch
        global match
        srch = request.POST['email']
        password = request.POST['password']
        if srch:
            match = Supplier.objects.filter(Q(email__icontains=srch) & Q(password__iexact=password))
            if match:
                for i in match:
                    name = str(i.shop_name)
                return render(request, 'dashboard.html', {'shop_name':name})
            else:
                return render(request, 'validate.html')
        else:
            return HttpResponseRedirect('/login/')
    return render(request, 'login.html')

def dashboard(request):
    name=srch
    for i in match:
        name = str(i.shop_name)
    shop_name = Supplier.objects.values('shop_name')
    return render(request, 'dashboard.html', {'shop_name': name})
'''
def form(request):
    name=srch
    for i in match:
        name = str(i.shop_name)
    shop_name = Supplier.objects.values('shop_name')
    return render(request, 'form.html', {'shop_name': name})
'''
def table(request):
    name=srch
    shop_name = Supplier.objects.values('shop_name')
    for k in match:
        category =  Category.objects.all()
    for i in match:
        name = str(i.shop_name)
        rec = Product.objects.filter(shop_name__shop_name=name)
    for j in match:
        name = str(j.shop_name)
        orders = Orders.objects.filter(shop_name__shop_name=name)
    data = { "details" : rec, 'shop_name': name, "orders": orders, "category": category}
    resp = render_to_response("table.html", data)
    return resp
         
def display(request):
    for i in match:
        test = str(i.shop_name)
        rec = Product.objects.filter(shop_name__shop_name=test)
    data = { "details" : rec}
    resp = render_to_response("display.html", data)
    return resp

def delete(request):
    pname = request.GET['pname']
    Product.objects.filter(product_name=pname).delete()
    return render(request, 'display.html')

def edit(request):
    pid = request.GET['id']
    edit = Product.objects.filter(id=pid)
    data = { "edit" : edit}
    #Product.objects.filter(product_name=pname).delete()
    return render(request, 'edit.html', data)

def update(request):
    if request.method == "POST":
        pid = request.POST.get('pid', '')
        pname = request.POST.get('pname', '')
        desc = request.POST.get('desc', '')
        pub_date = request.POST.get('pub_date', '')
        #image = request.POST.get('image', '')
        price = request.POST.get('price', '')
        Product.objects.filter(id=pid).update(product_name=pname, desc=desc, pub_date=pub_date, price=price)
    return render(request, 'update.html')

def add(request):
    pid = request.GET['sname']
    edit = Supplier.objects.filter(shop_name=pid)
    category = Category.objects.all()
    data = { "edit" : edit, "category": category }
    return render(request, 'add.html', data)

def addproduct(request):
    if request.method == "POST":
        sid = request.POST.get('sid', '')
        name = request.POST.get('name', '')
        category = request.POST.get('category', '')
        price = request.POST.get('price', '')
        description = request.POST.get('description', '')
        pubdate = request.POST.get('pubdate', '')
        price = request.POST.get('price', '')
        #image = request.POST.get('image', '')
        Product.objects.create(product_name=name, desc=description, pub_date=pubdate, category_id = category, price=price, shop_name_id=sid)
    return render(request, 'addproduct.html')
    
def profile(request):
    for i in match:
        name = str(i.shop_name)
        value = Supplier.objects.filter(shop_name=name)
    data = { "profile" : value, "shop_name": name }
    return render(request, 'form.html', data)

def profile_edit(request):
    if request.method == "POST":
        sid = request.POST.get('sid', '')
        sname = request.POST.get('shopname', '')
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        password = request.POST.get('password', '')
        Supplier.objects.filter(id=sid).update(shop_name=sname, address=address, phone=phone, password=password)
    return render(request, 'profile.html')

def contact(request):
    edit = Supplier.objects.all()
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'contact.html', {'edit':edit})