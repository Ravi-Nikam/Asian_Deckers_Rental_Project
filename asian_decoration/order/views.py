from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.shortcuts import render, HttpResponseRedirect, get_list_or_404, get_object_or_404 , redirect
from django.urls import reverse
from django.conf import settings
import stripe
from django.contrib import messages
from django.contrib.auth.models import User
from accounts.views import Address_info
# Create your views here.
from dec_app.models import rel_pro
from accounts.models import UserAddress
from cart_app.models import carts
from order.models import Order
from accounts.models import UserStripe , date_pro
from .models import Order, payment_stripe
from .utils import id_generator

import stripe
stripe_pub = settings.STRIPE_PUBLISHABLE_KEY
stripe.api_key = settings.STRIPE_SECRET_KEY

# `source` is obtained with Stripe.js; see https://stripe.com/docs/payments/accept-a-payment-charges#web-create-token
final_amount = 0

def payment_view(request):
    return render(request, 'account/stripe_payment.html')

def stripe_chk(request):
    print("==============================================================succ1")
    if request.method == "POST":
        ord = get_object_or_404(Order,order_id=request.session['order_id'])
        dates = get_object_or_404(date_pro,order_id=request.session['order_id'])
        print(ord.Sub_total)
        amt=Decimal(ord.get_final_amount())
        print("emlewkjlewjlfjlewjflwejoi",amt)
        try:
            if User.is_active:
                x = User.objects.filter(is_active=True).values_list('email', flat=True)
                email = x[0]
                try:
                    emails = email
                    print(emails)
                except Exception as e:
                    print("email error",e)

            token = request.POST['stripeToken']

            customer = stripe.Customer.create(
                email=emails,
                source=token,
            )
        except:
            customer = None
        if customer is not None:
            print("==============================================================succ2")
            try:
                charge = stripe.Charge.create(
                    amount=int(amt * 100),
                    currency="inr",
                    customer=customer,
                    description = "Chage for %s" %(request.user.username),
                    # source=token,
                )
                # other method
                # charge = stripe.Charge.create(
                #     amount=amt,
                #     currency="inr",
                #     source=token,
                # )
                # create the payment
                if charge["captured"]:
                    ord.status = "Finished"
                    ord.save()
                    del request.session['carts_id']
                    del request.session['item_total']
                    messages.success(request,"your order successfully placed")
                payment = payment_stripe()
                payment.stripe_charge_id = charge["id"]
                payment.email=emails
                print("464646465466464",payment.stripe_charge_id)
                payment.user = request.user
                print(payment.user)
                payment.amount = int(ord.get_final_amount() * 100)
                print(payment.amount)
                payment.save()
                messages.success(request, "your order was successfull")

                return render(request, 'checkout/payment_status.html', {'charge': charge, "ord":ord, "dates":dates})

            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.error(request, f"{err.get('message')}")
                return redirect("/")
            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.error(request,"Rate limit error")
                print("==============================================================suc4")
                return redirect("/")
            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                messages.error(request,"invalid parameter")
                print("==============================================================suc5")
                print("your error is",e)
                return redirect("/")
            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                print("==============================================================suc6")
                messages.error(request, "Not authantication")
                return redirect("/")
            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.error(request,"Network error")
                print("==============================================================suc7")
                return redirect("/")
            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                print("==============================================================suc8")
                messages.error(request,"something went wrong , you ware not charged please try again")
                return redirect("/")
                # yourself an email

            except Exception as e:
                print("==============================================================suc9")
                messages.error(request, "A serious error occur we notified after sometimes")
                return redirect("/")
                # Something else happened, completely unrelated to Stripe



def orders(request):
    template = 'checkout/payment_status.html'
    return render(request, template)

@login_required()
def checkout(request):
    try:
        the_id = request.session['carts_id']
        print("the_id", the_id)
        cart = carts.objects.get(id=the_id)
        print("cart", cart)
    except carts.DoesNotExist:
        the_id = None
        return HttpResponseRedirect(reverse("carts_det"))
    try:
        new_order = Order.objects.get(cart=cart)
        request.session['order_id'] = new_order.order_id
        ord = get_object_or_404(Order, order_id=request.session['order_id'])
    except Order.DoesNotExist:
        # create new order
        new_order = Order()
        new_order.cart =cart
        new_order.user = request.user
        new_order.order_id = id_generator()
        request.session['order_id'] = new_order.order_id
        print("request.session['order_id']",request.session['order_id'])
        new_order.save()
        ord = get_object_or_404(Order, order_id=request.session['order_id'])
    except:
        new_order = None
        # work on some error message
        return HttpResponseRedirect(reverse("carts_det"))
    if new_order is not None:    
        new_order.Sub_total = cart.total
        new_order.save()
        final_amount = new_order.get_final_amount()
        request.session['final_amt'] = final_amount
        print("56565111111111000000000000000000",final_amount)

    # run credit card
    # order status is finished  then delete cart_id and item_total session
    try:
        address_added = request.GET.get("redirect")
        print("order_info_redirect==>",address_added)
    except:
        address_added = None

    if address_added is not None:
        Addre =  Address_info(request)
    else:
        Addre = None

    current_addresses = UserAddress.objects.filter(user=request.user)
    billing_addresses = UserAddress.objects.get_billing_address(user=request.user)

    if new_order.status == "Finished":
        del request.session['carts_id']
        del request.session['item_total']
        return HttpResponseRedirect(reverse("home"))

    context = {'current_addresses': current_addresses, "billing_addresses":billing_addresses,"ord":ord}
    template = 'checkout/Checkout.html'
    return render(request, template, context)

