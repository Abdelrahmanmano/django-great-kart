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
    brand = models.CharField(max_length=100, verbose_name="Brand", blank=True)
    version = models.CharField(max_length=100, verbose_name="Version", blank=True)

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "Product here"
        verbose_name_plural = "Products"
        
    def get_url(self):
        return reverse('product_slug_detail', args=[self.category_id.slug, self.slug])

class VariationManager(models.Manager):
    def colors(self):
        return self.filter(variation_category='color', is_active=True)

    def sizes(self):
        return self.filter(variation_category='size', is_active=True)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    variation_category = models.CharField(max_length=100, verbose_name="Variation Category", choices=(('color', 'Color'), ('size', 'Size')))
    variation_value = models.CharField(max_length=100, verbose_name="Variation Value")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_date = models.DateTimeField(auto_now=True, verbose_name="Created Date")

    def __str__(self):
        return f"{self.variation_category}: {self.variation_value}"

    class Meta:
        verbose_name = "Variation"
        verbose_name_plural = "Variations"
        
    objects = VariationManager()