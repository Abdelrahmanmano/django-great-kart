from django.db import models
from store.models import Product

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.cart_id}"
        
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.FloatField(default=0.0)

    def __str__(self):
        return f"CartItem {self.product_id.product_name} in Cart {self.cart.id}"

    def save(self, *args, **kwargs):
        # Calculate total price based on product price and quantity
        print('calculating total price forice for cart item...')
        self.total = self.product_id.price * self.quantity
        super().save(*args, **kwargs)