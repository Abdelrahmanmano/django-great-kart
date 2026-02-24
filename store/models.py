from django.db import models
from category.models import Category
from django.urls import reverse

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True, verbose_name="Product Name")
    slug = models.SlugField(unique=True, verbose_name="URL Slug", blank=True)
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    stock = models.IntegerField(verbose_name="Stock Quantity")
    is_available = models.BooleanField(default=True, verbose_name="Is Available")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    modified_date = models.DateTimeField(auto_now=True, verbose_name="Modified Date")
    image = models.ImageField(upload_to='photos/products/%y/%m/%d', verbose_name="Product Image", blank=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Category")

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "Product here"
        verbose_name_plural = "Products"
        
    def get_url(self):
        return reverse('product_slug_detail', args=[self.category_id.slug, self.slug])
