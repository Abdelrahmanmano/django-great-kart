from django.shortcuts import render
from .models import Product
from category.models import Category
from cart.models import CartItem, Cart
from cart.views import _get_cart_id
from django.db.models import Q

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


# Create your views here.
def product_list(request):
    products = Product.objects.filter(is_available=True).order_by('-created_date')
    print('product abdooo', products)  # Debugging statement to check the retrieved products
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    is_in_cart = CartItem.objects.filter(cart__cart_id=_get_cart_id(request), product_id=product.id).exists()
    return render(request, 'store/product_detail.html', {'product': product, 'is_in_cart': is_in_cart})

def product_slug_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category_id__slug=category_slug, slug=product_slug)
        is_in_cart = CartItem.objects.filter(cart__cart_id=_get_cart_id(request), product_id=product.id).exists()
    except Product.DoesNotExist:
        product = None
    return render(request, 'store/product_detail.html', {'product': product, 'is_in_cart': is_in_cart})

def store(request, category_id=None, category_slug=None):
    products = Product.objects.filter(is_available=True).order_by('-created_date')
    categories = Category.objects.all()
    
    if category_id:
        products = products.filter(category_id=category_id)
    elif category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        except Category.DoesNotExist:
            pass
        
    paginator = Paginator(products, 3)  # Show 6 products per page
    page = request.GET.get('page')
    try:       
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'store/store.html', {'products': products, 'categories': categories})

def search(request):
    keyword = request.GET.get('keyword')
    print('keyword hereee', keyword)  # Debugging statement to check the received keyword
    products = Product.objects.filter(Q(product_name__icontains=keyword) | Q(description__icontains=keyword))
    print('search results hereee', products)  # Debugging statement to check the search results
    return render(request, 'store/store.html', {'products': products})