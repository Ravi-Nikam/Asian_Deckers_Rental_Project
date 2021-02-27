from django.contrib import admin

# Register your models here.
from .models import Order,payment_stripe


admin.site.register(Order)
admin.site.register(payment_stripe)
