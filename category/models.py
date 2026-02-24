from django.db import models
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True, verbose_name="Category Name")
    slug = models.SlugField(unique=True, verbose_name="URL Slug", blank=True)
    description = models.TextField(verbose_name="Description")
    cat_img = models.ImageField(upload_to='photos/categories/%y/%m/%d', verbose_name="Category Image", blank=True)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(f"{self.category_name} {self.description}")
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "Category here"
        verbose_name_plural = "Categories"
        
    def get_url(self):
        return reverse('store_by_slug', args=[self.slug])
