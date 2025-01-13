from django.urls import path
from . import views
from django.conf.urls import url

app_name = "shop_vendor"
urlpatterns = [
    path("", views.index, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("table/", views.table, name="table"),
    path("form/", views.profile, name="form"),
    path("add/", views.add, name="add"),
    url(r'^display/$', views.display, name="display"),
    url(r'^delete/$', views.delete, name="delete"),
    url(r'^edit/$', views.edit, name="edit"),
    url(r'^update/$', views.update, name="update"),
    url(r'^addproduct/$', views.addproduct, name="addproduct"),
    #path("update/", views.update, name="update"),
    url(r'^profile/$', views.profile, name="profile"),
    url(r'^profile_edit/$', views.profile_edit, name="profile_edit"),
    path("contact/", views.contact, name="ContactUs"),

]