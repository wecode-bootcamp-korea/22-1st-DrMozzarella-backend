from django.urls import path

from products.views import ProductDetailView, ProductsView

urlpatterns = [
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/products', ProductsView.as_view())
]