from .models import CartItem

def get_cart_count(request):
    cart_items = CartItem.objects.filter(cart__cart_id=request.session.session_key)
    print('cart count hereeeee', cart_items)
    return {'cart_count': sum(item.quantity for item in cart_items)}