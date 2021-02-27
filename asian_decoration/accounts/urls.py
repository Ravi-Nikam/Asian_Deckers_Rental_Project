from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.logout_, name='logout'),
    path('accounts/activate/<activation_key>', views.activation_view, name='activation_view'),
    path('checkout/', views.Address_info, name='checkout'),
    path('order/', views.order, name='order'),
    path('date_pro', views.date_pros, name='dates'),
    path('handlerequest/',views.handlerequest, name='HandleRequest'),
    path('paytm/', views.payment, name='payment'),
    # for password reset
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='account/Passwordreset.html'),
         name='Password_Reset' ),

    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/Password_reset_confirm.html'),
        name = 'password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),
]