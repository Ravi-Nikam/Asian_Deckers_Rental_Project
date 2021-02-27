from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_ca, name='carts_det'),
    path('Add_to_cart/<slug>', views.add_to_cart, name='pro_add_to_cart'),
]