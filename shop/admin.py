from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from shop.models import UserProfileInfo, User
from shop.forms import UserRegistrationForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.
from .models import Product, Contact, Orders, OrderUpdate, Category, Rating, Registration

@admin.register(Product)
class Product(ImportExportModelAdmin):
    list_display = ('product_name', 'category', 'desc', 'pub_date', 'shop_name', 'price')
    pass
@admin.register(Category)
class Category(ImportExportModelAdmin):
    list_display = ('category',)
    pass
#admin.site.register(Category)
#admin.site.register(Product)
admin.site.register(Contact)
#admin.site.register(Orders)
@admin.register(Orders)
class Orders(ImportExportModelAdmin):
    list_display = ('name', 'email', 'address', 'city', 'state', 'phone', 'shop_name')
    pass
admin.site.register(OrderUpdate)
admin.site.register(Rating)
admin.site.register(UserProfileInfo)
admin.site.register(Registration)


