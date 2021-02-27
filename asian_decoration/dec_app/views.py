from django.shortcuts import render, redirect, Http404, get_object_or_404, get_list_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Category_table
from .models import rel_pro
import re



# Create your views here.
def home(request):
    cat = Category_table.objects.all()
    return render(request, 'index.html', {'cate': cat})


def registration(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        con_pass = request.POST.get('con_password')
        btn = "join"
        if con_pass == password:
            print("x")
            if User.objects.filter(username=uname).exists():
                messages.info(request, 'user name is taken')
                page_message= "user name is taken"
                context = {"page_message": page_message}
                return render(request, 'registration.html', context)
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email is taken')
                page_message = "email is taken"
                context = {"page_message": page_message}
                return render(request, 'registration.html', context)
            else:
                user = User.objects.create_user(username=uname, email=email, password=password)
                user.save()
                messages.info(request, 'User registration successfully!! Please confirm your email')
                page_message = "User registration successfully!! Please confirm your email"
                context={ "submit_btn": btn, "page_message":page_message}
                return render(request, 'registration.html', context)
        else:
            messages.info(request, 'password is not match...')
            print("password is not match...")
            page_message = "password is not match..."
            context = {"page_message": page_message}
            return render(request, 'registration.html', context)
    else:
        return render(request, 'Registration.html')


def login(request):
    if request.method == "POST":
        user = request.POST['Luname']
        password = request.POST['Lpassword']
        btn="Login"
        user = auth.authenticate(username=user, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user_id'] = user
            print(request.session['user_id'])
            context = {"submit_btn": btn}
            messages.success(request, 'User Logged In successfully!! Welcome ')
            return redirect('/', context)
        else:
            messages.info(request, 'invalid username or Password')
            return redirect('registration')
    else:
        return render(request, 'registration')


def product(request):
    cat = Category_table.objects.all()
    return render(request, 'category.html', {'cate': cat})


def cat_rel_pro(request, slug):
    try:
        # products = rel_pro.objects.filter(slug=slug)
        # getting the all category related product
        category = get_object_or_404(Category_table, slug=slug)
        print(category)
        # we filter it into rel_pro on categoty
        products = rel_pro.objects.filter(category=category)
        print(products)
        return render(request, 'product.html', {'products': products})
    except:
        Http404


def pro_description(request, slug):
    product_desc = get_list_or_404(rel_pro, slug=slug)
    template = 'product_description.html'
    context = {'product_desc': product_desc}
    return render(request, template, context)


def search(request):
    try:
        q = request.GET.get('search')
    except:
        q = None
    if q:
        products = rel_pro.objects.filter(image__icontains=q)
        context = {'query': q, 'products': products}
        template = 'result.html'
    else:
        context = {'query': q}
        template = 'index.html'
    return render(request, template, context)


def about_us(request):
    return render(request, 'About_us.html')




