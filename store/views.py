from django.shortcuts import render
from .models import Product
from category.models import Category

# Create your views here.
def product_list(request):
    products = Product.objects.filter(is_available=True).order_by('-created_date')
    print('product abdooo', products)  # Debugging statement to check the retrieved products
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

def product_slug_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category_id__slug=category_slug, slug=product_slug)
    except Product.DoesNotExist:
        product = None
    return render(request, 'store/product_detail.html', {'product': product})

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
    

    return render(request, 'store/store.html', {'products': products, 'categories': categories})