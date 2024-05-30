from django.urls import path
from apps.products.api.views.product_views import (ProductListAPIView, ProductCreateAPIView, ProductRetriveAPIView, 
    ProductDestroyAPIView, ProductUpdateAPIView, ProductListCreateAPIView, ProductRetrieveUpdateDestroyApiView
)

urlpatterns = [
    path('products/list/', ProductListAPIView.as_view(), name='products_list'),
    path('products/create/', ProductCreateAPIView.as_view(), name='products_create'),
    path('products/retrieve/<int:pk>', ProductRetriveAPIView.as_view(), name='product_retrieve'),
    path('products/destroy/<int:pk>', ProductDestroyAPIView.as_view(), name='product_destroy'),
    path('products/update/<int:pk>', ProductUpdateAPIView.as_view(), name='product_update'),
    path('products/list_create/', ProductListCreateAPIView.as_view(), name='products_list_create'),
    path('products/retrieve_update_destroy/<int:pk>', ProductRetrieveUpdateDestroyApiView.as_view(), name='products_retrieve_update_destroy'),
]