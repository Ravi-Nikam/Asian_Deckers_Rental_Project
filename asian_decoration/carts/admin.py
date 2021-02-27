from django.contrib import admin

# Register your models here.
from .models import carts, cart_item


class cart_admin(admin.ModelAdmin):
    class Meta:
        model = carts


admin.site.register(carts, cart_admin)

admin.site.register(cart_item)
