from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Category, Product
from .forms import ProductAddForm


# Homepage
def home_view(request):
    template = 'core/home.html'
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


@login_required
def product_add_view(request):
    template = 'core/sell.html'
    context = {}
    seller = request.user
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
