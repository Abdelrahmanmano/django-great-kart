from django.contrib import admin
from .models import Product#, Variation, ReviewRating

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'is_available', 'created_date', 'modified_date', 'image')  # Display these fields in the admin list view
    prepopulated_fields = {'slug': ('product_name',)}  # Automatically populate slug based on product_name and description
    readonly_fields = ('created_date', 'modified_date')  # Make created_date and modified_date readonly
    ordering = ('-created_date',)  # Order products by created_date in descending order

admin.site.register(Product, ProductAdmin)

