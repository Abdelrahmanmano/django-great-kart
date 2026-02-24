from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('store/', views.store, name='store'),
    path('store/<int:category_id>/', views.store, name='store_by_category'),
    path('store/<slug:category_slug>/', views.store, name='store_by_slug'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_slug_detail, name='product_slug_detail'),
]
