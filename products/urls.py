from django.urls import path

from products.views import ProductDetailView, ProductsView

urlpatterns = [
    path('', ProductsView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view())
]
