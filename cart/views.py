from django.shortcuts import render, redirect
from .models import Cart, CartItem
from store.models import Product, Variation

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
        cart_item_id = request.GET.get('cart_item_id')
        variation_lst = [] 
        if request.method == 'POST':
            color = request.POST.get('color')
            size = request.POST.get('size')
            for key, value in request.POST.items():
                variation_obj = Variation.objects.filter(product=product, variation_category__iexact=key, variation_value__iexact=value).first()
                if variation_obj:
                    variation_lst.append(variation_obj)
        elif cart_item_id:
            cart_item = CartItem.objects.get(id=cart_item_id)
            variation_lst = list(cart_item.variations.all())

        # Check if the product is in stock
        if product.stock <= 0:
            return redirect(request.META.get('HTTP_REFERER', 'cart'))  # Stay on the current page

        # Get or create the cart
        cart, _ = Cart.objects.get_or_create(cart_id=_get_cart_id(request))

        # Check if a cart item with the same product and variations exists
        existing_cart_item = None
        cart_items = CartItem.objects.filter(cart=cart, product_id=product)
        
        for item in cart_items:
            item_variations = set(item.variations.all())
            if item_variations == set(variation_lst):
                existing_cart_item = item
                break
        
        if existing_cart_item:
            # Update quantity if the same item with same variations exists
            existing_cart_item.quantity += 1
            existing_cart_item.save()
        else:
            # Create a new cart item
            cart_item = CartItem.objects.create(cart=cart, product_id=product, quantity=1)
            if variation_lst:
                for variation in variation_lst:
                    cart_item.variations.add(variation)
            cart_item.save()

        # Update stock and save changes
        product.stock -= 1
        product.save()

    except Product.DoesNotExist:
        # Handle the case where the product does not exist
        return redirect(request.META.get('HTTP_REFERER', 'cart'))  # Stay on the current page

    return redirect('cart')

def remove_qty_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    product = cart_item.product_id
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


def place_order(request):
    # Example logic to place an order
    cart_items = CartItem.objects.filter(cart__cart_id=_get_cart_id(request))
    # Here you would typically create an Order object and save the order details
    # For this example, we'll just clear the cart
    cart_items.delete()
    return render(request, 'cart/order_placed.html')