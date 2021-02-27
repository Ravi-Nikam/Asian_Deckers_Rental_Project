from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name="login"),
    path('product/', views.product, name='product'),
    path('About_us/', views.about_us, name='about_us'),
    path('cat_rel_pro/<slug>', views.cat_rel_pro, name='cat_rel_pro'),
    path('pro_desc/<slug>', views.pro_description, name='product_description'),
    path('s/', views.search, name='search'),
]
