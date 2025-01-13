from django import forms
from shop.models import UserProfileInfo
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password', 'email')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 32,
    )
    email = forms.CharField(
        required = True,
        label = 'Email',
        max_length = 32,
    )
    password = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = forms.PasswordInput()
    )
    verify = forms.CharField(
        required = True,
        label = 'Confirm Password',
        max_length = 32,
        widget = forms.PasswordInput()
    )
    city = forms.CharField(max_length=15)
    mobile = forms.CharField(max_length=15)
    pin_code = forms.CharField(max_length=15)
   

