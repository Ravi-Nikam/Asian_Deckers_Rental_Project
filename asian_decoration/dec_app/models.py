from django.db import models
from django.urls import reverse


# Create your models here.
# create category table into database.

class Category_table(models.Model):
    cname = models.CharField(max_length=200, primary_key=True)
    slug = models.SlugField(max_length=200, unique=True, default='')  # slug is a unique for category.
    cat_img = models.ImageField(upload_to="category_list", default="default.png")
    category_active = models.BooleanField(default=True)

    def __str__(self):
        return self.cname

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])


def images_upl(instance, filename):
    return 'cat_rel_product/{0}/{1}'.format(instance.category.cname, filename)


class rel_pro(models.Model):
    category = models.ForeignKey(Category_table, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, blank=True, unique=True)
    image = models.ImageField(upload_to=images_upl, blank=True)
    description = models.TextField(blank=True)
    price = models.IntegerField(default=0)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    no_days=models.IntegerField(default=0)
    dates=models.CharField(max_length=100)

    def __str__(self):
        return self.name + "****" + self.slug

    def get_absolute_url(self):
        return reverse("cat_rel_pro", kwargs={"slug": self.slug})