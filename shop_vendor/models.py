from django.db import models

# Create your models here.
class Supplier(models.Model):
    supplier_id = models.AutoField
    shop_name = models.CharField(max_length=300)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    phone = models.CharField(max_length=11, default="")
    password = models.CharField(max_length=6, default="abc")
    geolocation = models.CharField(max_length=300, default="https://www.google.com/maps/dir///@15.0172605,76.3178081,7z")

    def __str__(self):
        return '%s' % (self.shop_name)
