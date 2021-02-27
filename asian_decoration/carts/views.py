from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, get_list_or_404
from django.urls import reverse
# Create your views here.
from .models import carts, cart_item
from dec_app.models import rel_pro


def view_ca(request):
    try:
        the_id = request.session['carts_id']
    except:
        the_id = None
    if the_id:
        carts1 = carts.objects.get(id=the_id)
        context = {'carts1': carts1}
    else:
        empty_message = "your cart is empty"
        context = {'carts1': True, "empty_message": empty_message}
    templates = 'cart/cart_view.html'
    return render(request, templates, context)


def add_to_cart(request, slug):
    request.session.set_expiry(120000)
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

    carts1 = carts.objects.get(id=the_id)
    print("1", carts1)
    try:
        # get_obj_or_404(where you want to get , what get) mthod get only one object
        # Product = rel_pro.objects.get(slug=slug)  or
        Product = get_object_or_404(rel_pro, slug=slug)
        print("2", Product)
    except Product.DoesNotExist:
        pass
    except:
        pass
    # below code creating cart item for us
    # it returns ("model object", "true/false")
    Cart_item, created = cart_item.objects.get_or_create(Product=Product)
    if created:
        print("created")
    # end
    if not Cart_item in carts1.items.all():
        # adding product into  the cart
        carts1.items.add(Cart_item)
        print("3", carts1)
    else:
        # remove product into cart
        carts1.items.remove(Cart_item)
        print("4", carts1)

    # cart all item total
    new_total = 0.00
    for itm in carts1.items.all():
        line_total = float(itm.Product.price) * round(itm.quantity, 2)
        print(line_total)
        new_total += line_total
        print(new_total)

    # count the total number of itm in cart
    request.session['item_total'] = carts1.items.all().count()
    print(carts1.rel_pros.all().count())
    carts1.total = new_total
    carts1.save()

    return HttpResponseRedirect(reverse("carts_det"))
