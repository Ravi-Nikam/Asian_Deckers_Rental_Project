from django.contrib import admin

# Register your models here.
from .models import carts, CartItem


class cartAdmin(admin.ModelAdmin):
    class Meta:
        model = carts


admin.site.register(carts, cartAdmin)

admin.site.register(CartItem)
