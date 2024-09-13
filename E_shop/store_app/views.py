from django.shortcuts import render,redirect
from store_app.models import Product,Categories,Filter_Price,Color,Brand,Contact_us
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart






# Create your views here.

def HOME(request):
    product = Product.objects.filter(status='Publish')
    context = {
        'product': product
    }
    return render(request,'Main/index.html',context)

def BASE(request):
    return render(request,'Main/base.html')


def PRODUCT(request):
    # product = Product.objects.filter(status='Publish') previously added but not required now
    categories = Categories.objects.all()
    filter_price = Filter_Price.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()

    category_id = request.GET.get('category_id') #for filtering categories wise products
    filter_price_id = request.GET.get('filter_price_id') #for filtering price wise products
    color_id = request.GET.get('color_id') #for filtering color wise products
    brand_id = request.GET.get('brand_id') #for filtering brand wise products
    AtoZ_id = request.GET.get('AtoZ')
    ZtoA_id = request.GET.get('ZtoA') 
    low_to_high_id = request.GET.get('low_to_high')
    high_to_low_id = request.GET.get('high_to_low')
    new_product_id = request.GET.get('new_product')
    old_product_id = request.GET.get('old_product')
    

    if category_id:
        product = Product.objects.filter(status='Publish',categories=category_id)
    elif filter_price_id:
        product = Product.objects.filter(status='Publish',filter_price=filter_price_id)
    elif color_id:
        product = Product.objects.filter(status='Publish',color=color_id)
    elif brand_id:
        product = Product.objects.filter(status='Publish',brand=brand_id)
    elif AtoZ_id:
        product = Product.objects.filter(status='Publish').order_by('name')
    elif ZtoA_id:
        product = Product.objects.filter(status='Publish').order_by('-name')
    elif low_to_high_id:
        product = Product.objects.filter(status='Publish').order_by('price')
    elif high_to_low_id:
        product = Product.objects.filter(status='Publish').order_by('-price')
    elif new_product_id:
        product = Product.objects.filter(condition='New')
    elif old_product_id:
        product = Product.objects.filter(condition='Old')
    else:
        product = Product.objects.filter(status='Publish')


    context = {
        'product': product,
        'categories': categories,
        'filter_price': filter_price,
        'color': color,
        'brand': brand,
    }
    return render(request,'Main/product.html',context)


def SEARCH(request):
    query = request.GET.get('query')
    product = Product.objects.filter(name__icontains=query)

    context = {
        'product':product,
    }

    return render(request,'Main/search.html',context)

def PRODUCT_DETAILS(request,pid):
    prod = Product.objects.filter(id=pid).first()
    context = {
        'prod':prod,
    }
    
    return render(request, 'Main/product_details.html',context)

def CONTACT(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact_us(name=name, email=email, subject=subject, message=message)
        contact.save()
        return redirect('/')

    return render(request,'Main/contact.html')

def REGISTER(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        customer = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email)
        customer.set_password(password)
        customer.save()

        return redirect('/register')
        
    return render(request,'Registration/register.html')

def LOGIN(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/login')
    
    return render(request,'Registration/register.html')

def LOGOUT(request):
    logout(request)
    return redirect('/')

@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("/")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')

def CHECKOUT(request):
    return render(request,'cart/checkout.html')

