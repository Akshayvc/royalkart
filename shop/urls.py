from django.urls import path
from . import views
from django.conf.urls import url

app_name = "shop"
urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    url(r'^search/$', views.search, name="search"),
    path("register/", views.register, name="register"),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profile/$', views.profile, name="profile"),
    url(r'^basic/$', views.basic, name="basic"),
    url(r'^basics/$', views.basics, name="basics"),
]
