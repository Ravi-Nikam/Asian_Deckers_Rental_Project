from django.db import models
from decimal import Decimal
from django.conf import settings
from django.contrib.auth import get_user_model
# Create your models here.
from  cart_app.models import carts

User = get_user_model()

STATUS_CHOICES = (
    ("started", "started"),
    ("Abandoned", "Abandoned"),
    ("Finished", "Finished"),
)

#tuple


class Order(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    Sub_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places=2)
    tax_total = models.DecimalField(default=.00, max_digits=1000, decimal_places=2)
    final_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places=2)
    order_id = models.CharField(max_length=120,  default='ABC', unique=True)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default="started")
    cart = models.ForeignKey(carts, on_delete=models.CASCADE)


    def __str__(self):
        return self.order_id

    def get_final_amount(self):
        instance = Order.objects.get(id=self.id)
        two_places = Decimal(10) ** -2
        instance.tax_total = Decimal(Decimal("0.08") * Decimal(self.Sub_total)).quantize(two_places)
        instance.final_total = Decimal(self.Sub_total) + Decimal(self.tax_total)
        instance.save()
        return self.final_total


class payment_stripe(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,blank=True,null=True)
    amount = models.DecimalField(default=10.99, max_digits=1000, decimal_places=2)
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return str(self.user)
