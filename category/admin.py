from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug', 'description', 'cat_img')
    prepopulated_fields = {'slug': ('category_name',)}  # Automatically populate slug based on category_name and description

admin.site.register(Category, CategoryAdmin)
