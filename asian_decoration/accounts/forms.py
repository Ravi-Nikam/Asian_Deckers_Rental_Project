from django import forms
from django.contrib.auth import get_user_model
from .models import UserAddress

User = get_user_model()


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ["user", "firstname", "lastname", "address", "city" ,"state", "zip_code" , "phone","shipping","billing"]

