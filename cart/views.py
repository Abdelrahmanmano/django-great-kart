from django.shortcuts import render, redirect
from .models import Cart, CartItem
from store.models import Product

# Create your views here.
def cart(request):
    cart_items = CartItem.objects.filter(cart__cart_id=_get_cart_id(request))
    print('cart item hereeeee', list(cart_items.values())) 
    return render(request, 'cart/cart.html', {'cart_items': cart_items})

def add_to_cart(request):
    # Example logic to add item to cart
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        # In a real app, you would save this to the database
        cart_item = Cart.objects.create(product_id=product_id, quantity=quantity)
    return render(request, 'cart/cart.html')

def _get_cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

def add_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        if product.stock <= 0:
            return redirect('cart')  # Optionally, add a message for the user
        cart, _ = Cart.objects.get_or_create(cart_id=_get_cart_id(request))
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product)
        if created:
            cart_item.quantity = 1
        else:
            cart_item.quantity += 1
        product.stock -= 1
        product.save()
        cart_item.save()
    except Product.DoesNotExist:
        return redirect('cart')  # Optionally, add a message for the user
    return redirect('cart')

def remove_qty_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(cart_id=_get_cart_id(request))
    cart_item = CartItem.objects.get(cart=cart, product_id=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    product.stock += 1
    product.save()
    return redirect('cart')

def remove_from_cart(request, cart_item_id):
    # Example logic to remove item from cart
    if request.method == 'POST':
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.product_id.stock += cart_item.quantity  # Restock the product
        cart_item.product_id.save()
        cart_item.delete()
    return redirect('cart')

