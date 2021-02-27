from django.db import models
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, Http404, get_object_or_404, HttpResponse
from django.contrib.auth import logout
from .models import EmailConfirmed, paytm, date_pro
from .models import UserAddress, UserDefaultAddress
from .PayTm import Checksum
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib import messages
from order.models import Order
from django.views.decorators.csrf import csrf_exempt
User = get_user_model()
MERCHANT_KEY = 'NimklH_srEi9%&@d';

# Create your views here.
import re


def logout_(request):
    logout(request)
    messages.success(request, 'User Logged out successfully!! Feel free to login again! ')
    return HttpResponseRedirect('/')


# for stripe

# for stripe
try:
    stripe_pub = settings.STRIPE_PUBLISHABLE_KEY
except:
    print("error**********************************************************************")
    raise NotImplementedError

# activation view

SH1_RE = re.compile('^[a-f0-9]{40}$')


def activation_view(request, activation_key):
    print("****************************************************************************************")
    if SH1_RE.search(activation_key):
        print("activation is real")
        try:
            user_confirmed = EmailConfirmed.objects.get(activation_key=activation_key)
        except EmailConfirmed.DoesNotExist:
            user_confirmed = None
            messages.success(request, "Thare was an error with your request!")
        if user_confirmed is not None and not user_confirmed.confirmed:
            messages.success(request, "confirmation successful! Welcome")
            page_message = " confirmation successful! Welcome "
            user_confirmed.confirmed = True
            user_confirmed.save()
        elif user_confirmed is not None and user_confirmed.confirmed:
            messages.success(request, 'Aleredy confirmed')
            page_message = " Aleredy confirmed "
        else:
            page_message = ""
        context = {"page_message": page_message}
        return render(request, "account/activation.html", context)
    else:
        raise Http404

@login_required()
def Address_info(request):
    if request.method == 'POST':
        user = request.session['user_id']
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        address = request.POST.get('Address') + " " + request.POST.get('Address2')
        city = request.POST.get('city')
        # amount = request.session['cart_total']
        phone = request.POST.get('num')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        billing = request.POST.get('sameadr') == "on"
        default = request.POST.get('Default')
        order = UserAddress(user=user, firstname=firstname, lastname=lastname, address=address,
                            city=city, phone=phone, state=state, zip_code=zip_code, billing=billing)
        print(default)
        print("----", order)
        print(request.GET)
        try:
            redirect = request.GET.get("redirect")
        except:
            redirect = None
        if order is not None:
            if default == "Default":
                # taking the address user vise
                default_address, created = UserDefaultAddress.objects.get_or_create(user=request.user)
                order.user = request.user
                order.save()
                default_address.shipping = order
                default_address.billing = order
                default_address.save()
                default = "None"
            if redirect is not None:
                return HttpResponseRedirect(reverse(str(redirect)) + "?address_added=True")
        else:
            raise Http404


def payment(request):
    amount = request.session['final_amt']
    order_id = request.session['order_id']
    if User.is_active:
        x = User.objects.filter(is_active=True).values_list('email', flat=True)
        print("list", x)
        emails = x[0]
        pay = paytm(order_id=order_id, Email=emails, amount=amount)
        pay.save()
    param_dict = {
        # marchent id
        'MID': 'seWOqm24474885361610',
        'ORDER_ID': order_id,
        'TXN_AMOUNT': str(amount),
        'CUST_ID': emails,
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': 'http://127.0.0.1:8000/account/handlerequest/',
    }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return render(request, 'account/paytm.html', {"param_dict": param_dict})
    # request paytm to transfer amount to your account after payment by user

@csrf_exempt
def handlerequest(request):
    # to solve obj refer before assing enter your marchant id
    form = request.POST
    #ord = get_object_or_404(Order)
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            request.session['item_total'] = 0
            print("order Succesful")
        else:
            print("order was not successful because" + response_dict['RESPMSG'])
    return render(request, 'checkout/payment_status.html', {'response': response_dict})
    # paytm will send you post request here
    pass


def order(request):
    return render(request, "checkout/order.html")


def passwordreset(request):
    return render(request, 'account/Passwordreset.html')


def passwordreset_done(request):
    return render(request, 'account/Passwordreset_done.html')


def date_pros(request):
    redirect = request.GET.get("redirect")
    if redirect == "order_info":
        order_ids = request.session['order_id']
        pass
    else:
        orde = get_object_or_404(Order,order_id=request.session['order_id'])
        order_ids = orde
    if request.method == 'POST':
        if User.is_active:
            x = User.objects.filter(is_active=True).values_list('email', flat=True)
            print("list", x)
            emails = x[0]

        Str_date = request.POST.get('Str_date')
        End_date = request.POST.get('End_date')

        print(emails)
        print(order_ids)
        print(Str_date)
        print(End_date)
        dates = date_pro(order_id=order_ids, Email=emails, Str_date=Str_date, End_date=End_date)
        dates.save()

    return HttpResponseRedirect(reverse('order_info'))
