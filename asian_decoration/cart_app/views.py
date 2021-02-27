from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
# models
from .models import carts, CartItem
from dec_app.models import rel_pro
# Create your views here.


def view_ca(request):
    try:
        the_id = request.session['carts_id']
        cart = carts.objects.get(id=the_id)
    except:
        the_id = None
    if the_id:
        # cart = carts.objects.get(id=the_id)
        context = {'cart': cart}
    else:
        empty_message = "your cart is empty"
        context = {'cart': True, "empty_message": empty_message}

    templates = 'cart/cart_view.html'
    return render(request, templates, context)


def add_to_cart(request, slug):
    request.session.set_expiry(120000)
    try:
        qty = request.GET.get('qty')
        update_qty = True
    except:
        qty = None
        update_qty = False
    try:
        # aleredy exist person
        the_id = request.session['carts_id']
        print(the_id)
    except:
        # create new id and session
        new_cart = carts()
        new_cart.save()
        request.session['carts_id'] = new_cart.id
        the_id = new_cart.id

    cart = carts.objects.get(id=the_id)
    print("1", cart)
    try:
        # product = rel_pro.objects.get(slug=slug)
        product = get_object_or_404(rel_pro, slug=slug)
    except rel_pro.DoesNotExist:
        pass
    except:
        pass
    Cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        print("created")
    if update_qty and qty:
        if int(qty) == 0:
            Cart_item.delete()
        else :
            Cart_item.quantity = qty
            Cart_item.save()
    else:
        pass
    #if not Cart_item in cart.items.all():
    #     cart.items.add(Cart_item)
    #else:
    #     cart.items.remove(Cart_item)
    new_total = 0.00
    for item in cart.cartitem_set.all():
        line_total = item.product.price * item.quantity
        new_total += line_total

    request.session['item_total'] = cart.cartitem_set.all().count()
    cart.total = new_total
    request.session['cart_total_'] = cart.total
    cart.save()

    return HttpResponseRedirect(reverse("carts_det"))