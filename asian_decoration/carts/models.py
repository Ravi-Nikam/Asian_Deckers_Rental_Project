from django.db import models
from dec_app.models import rel_pro


# import model of product


# foreign key of carts

class cart_item(models.Model):
    Product = models.ForeignKey(rel_pro, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class carts(models.Model):
    items = models.ManyToManyField(cart_item, null=True, blank=True)
    rel_pros = models.ManyToManyField(rel_pro, null=True, blank=True)
    total = models.DecimalField(max_length=100, decimal_places=2, max_digits=5, default=0.00)
    available = models.BooleanField(default=True)
