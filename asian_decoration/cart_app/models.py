from django.db import models
from django.urls import reverse

# Create your models here.
from dec_app.models import rel_pro


class carts(models.Model):
    # items = models.ManyToManyField(CartItem, null=True, blank=True)
    # rel_pros = models.ManyToManyField(rel_pro, null=True, blank=True)
    total = models.DecimalField(decimal_places=2, max_digits=100, default=0.00)
    available = models.BooleanField(default=True)


class CartItem(models.Model):
    cart = models.ForeignKey(carts, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(rel_pro, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    line_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places=2)

    def __unicode__(self):
        try:
            return str(self.cart.id)
        except:
            return  self.product.name
