from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='order_info'),
    path('order/', views.orders, name='user_order'),
    path('stripe_payment/',views.payment_view, name='payment_view'),
    path('stripe_check/', views.stripe_chk, name='stripe_chk'),
]