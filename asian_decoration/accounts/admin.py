from django.contrib import admin

# Register your models here.
from .models import UserStripe, EmailConfirmed, UserAddress , UserDefaultAddress, paytm, date_pro

admin.site.register(UserStripe)
admin.site.register(EmailConfirmed)
admin.site.register(date_pro)


class UserAddressAdmin(admin.ModelAdmin):
    class Meta:
        model = UserAddress


admin.site.register(UserAddress, UserAddressAdmin)
admin.site.register(UserDefaultAddress)
admin.site.register(paytm)