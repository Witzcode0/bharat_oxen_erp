from django.urls import path
from apps.products.views import (
    add_unit, list_units,
    add_product, list_products, product_detail,
    delete_product, product_list_api
)

urlpatterns = [
    # Unit
    path('unit/add/', add_unit),
    path('unit/list/', list_units),

    # Product CRUD
    path('products/', product_list_api, name='product-list-api'),
    path('product/add/', add_product),
    path('product/list/', list_products),
    path('product/<uuid:pk>/', product_detail),
    path('product/delete/<uuid:pk>/', delete_product),
]
