from django.urls import path
from products.views import ProductsView    

urlpatterns = [
    path('/products', ProductsView.as_view())
]
