from accounts.models import CongoUserProfile
from .forms import ProductAddForm, AddToCartForm, AddressForm
from .models import Category, Product, OrderItem, Address, Order, Payment
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required

import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


# Homepage
def home_view(request):
    template = 'core/home.html'
    context = {}
    return render(request, template, context)


def categories_view(request):
    template = 'core/categories.html'
    context = {}
    categories = list(Category.objects.all())
    categories_size = len(categories)
    '''
    Two categories lists for two rows of categories - it's an adhoc solution.
    If we don't separate categories into two rows, then the UI works fine in mobile view
    but it gets messed up on desktop view.
    '''
    context['categories1'] = categories[0:categories_size // 2]
    context['categories2'] = categories[categories_size // 2:]
    return render(request, template, context)


# Category View - Viewing products for a particular category
def category_view(request, category):
    template = 'core/category.html'
    context = {}
    product_category = Category.objects.get(title=category)
    products = list(Product.objects.filter(category=product_category))
    products_size = len(products)
    # Doing the same thing as for categories in above view
    product_list = []
    for i in range(0, products_size, 4):
        product_list.append(products[i:i + 4])
    context['category'] = product_category
    context['product_list'] = product_list
    return render(request, template, context)


# Product Detail View - View the details of selected product
def product_detail_view(request, category, product_id):
    template = 'core/product_detail.html'
    context = {}

    # fetch the requested product and its seller details
    product = Product.objects.get(id=product_id)
    seller = product.seller
    seller_profile = CongoUserProfile.objects.filter(congo_user=seller)
    if seller_profile.count() > 0:
        seller_profile = seller_profile.first()

    # fetch other products by this seller to dsiaplay as recommendations
    other_products = Product.objects.filter(seller=seller)[:5]

    # populate context meta
    context['product'] = product
    context['category'] = product.category
    context['seller'] = seller_profile
    context['other_products'] = other_products

    if request.POST:
        form = AddToCartForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.buyer = request.user
            order_item.item = product
            order_item.total_price = (order_item.quantity * product.price)
            order_item.save()
            return redirect('cart')
    else:
        add_to_cart_form = AddToCartForm()
        context['form'] = add_to_cart_form
        return render(request, template, context)


@login_required
def product_add_view(request):
    template = 'core/sell.html'
    context = {}
    seller = request.user
    # allow only authenticated people to add products
    if not seller.is_authenticated:
        template = 'error_404.html'
    if request.POST:
        product_form = ProductAddForm(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.seller = seller
            product.save()
            return redirect('home')
        else:
            context['form'] = product_form
    else:
        product_form = ProductAddForm()
        context['form'] = product_form
    return render(request, template, context)


@login_required
def cart_view(request):
    template = 'core/cart.html'
    context = {}
    buyer = request.user
    cart_items = OrderItem.objects.filter(buyer=buyer, ordered=False)
    total_price = 0.0
    for item in cart_items:
        total_price += item.total_price
    context['items'] = cart_items
    context['total_price'] = total_price
    return render(request, template, context)


@login_required
def shipping_address_view(request):
    template = 'core/address.html'
    context = {}
    if request.POST:
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.congo_user = request.user
            address.save()
            return redirect('checkout')
        else:
            context['address_form'] = address_form
    else:
        address_form = AddressForm()
        context['address_form'] = address_form
    return render(request, template, context)


@login_required
def checkout_view(request):
    template = 'core/payment.html'
    context = {}

    # fetch address for this order
    address = Address.objects.filter(congo_user=request.user)
    address = address.first()

    # fetch buyer details
    buyer = request.user

    # fetch items ordered
    cart_items = OrderItem.objects.filter(buyer=buyer, ordered=False)

    # calculate total order price
    total_price = 0.0
    for item in cart_items:
        total_price += item.total_price
    amount = int(total_price)

    # populate context
    context['address'] = address
    context['total_price'] = amount
    context['stripe_amount'] = amount * 100
    context['key'] = settings.STRIPE_PUBLISHABLE_KEY

    # fetch order object
    order = Order.objects.create(buyer=request.user, ordered=False)

    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=amount,
            currency='inr',
            description='CongoCart',
            source=request.POST['stripeToken']
        )

        payment = Payment()
        payment.stripe_charge_id = charge['id']
        payment.congo_user = request.user
        payment.amount = amount
        payment.save()

        # assign the payment to the order and make all the items ordered
        order.ordered = True
        order.payment = payment
        order.shipping_address = address
        for item in cart_items:
            item.ordered = True
            order.items.add(item)
            item.save()
        order.save()
        return render(request, 'core/charge.html', context)

    return render(request, template, context)


@login_required
def charge_view(request):
    cart_items = OrderItem.objects.filter(buyer=request.user, ordered=False)
    total_price = 0.0
    for item in cart_items:
        total_price += item.total_price
    amount = total_price * 100
    context = {}
    context['total_price'] = total_price
    return render(request, 'core/charge.html', context)


def profile_view(request):
    template = 'core/profile.html'
    context = {}
    profile = CongoUserProfile.objects.get(congo_user=request.user)
    context['profile'] = profile
    return render(request, template, context)