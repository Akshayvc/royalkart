from django.db import models
from shop_vendor.models import Supplier
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Category(models.Model):
    category_id = models.AutoField
    category = models.CharField(max_length=50, default="")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category
    

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.ForeignKey(
        Category, default=1, verbose_name="Category", on_delete=models.SET_DEFAULT)
    #subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=3000)
    pub_date = models.DateField('Published', blank=True, null=True)
    image = models.ImageField(upload_to="shop/images",
                              default="", blank=True, null=True)
    # ,,stock,supplierid,category,shopname,ratings
    shop_name = models.ForeignKey(Supplier, default=1, verbose_name="Supplier", on_delete=models.SET_DEFAULT)
    count = models.IntegerField(default=10)
    rate = models.IntegerField(default=1)
    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return '%s %s' % (self.product_name, self.shop_name)


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name

class Registration(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    mobile = models.CharField(max_length=70, default="")
    city = models.CharField(max_length=20)
    pincode = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    confirm = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=11, default="")
    shop_name = models.ForeignKey(Supplier, default=1, verbose_name="Supplier", on_delete=models.SET_DEFAULT)

    class Meta:
        verbose_name_plural = "Orders"
    
    def __str__(self):
        return self.name


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."


class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(
        Product, default=1, verbose_name="Product Id", on_delete=models.SET_DEFAULT)
    ratings = models.IntegerField(default=0)


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    
    def __str__(self):
        return self.user.username


