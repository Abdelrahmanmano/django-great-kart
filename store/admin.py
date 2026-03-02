from django.contrib import admin
from .models import Product , Variation

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'is_available', 'created_date', 'modified_date', 'image')  # Display these fields in the admin list view
    prepopulated_fields = {'slug': ('product_name',)}  # Automatically populate slug based on product_name and description
    readonly_fields = ('created_date', 'modified_date')  # Make created_date and modified_date readonly
    ordering = ('-created_date',)  # Order products by created_date in descending order
    
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'created_date')  # Display these fields in the admin list view
    list_filter = ('variation_category', 'is_active')  # Add filters for variation_category and is_active
    search_fields = ('product__product_name', 'variation_value')  # Add search functionality for product name and variation value
    readonly_fields = ('created_date',)  # Make created_date readonly
    ordering = ('-created_date',)  # Order variations by created_date in descending order
    list_editable = ('is_active',)  # Allow is_active to be editable in the list view

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)

