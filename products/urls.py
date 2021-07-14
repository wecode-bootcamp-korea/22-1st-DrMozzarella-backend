from django.urls import path
from products.views import ProductsView    

urlpatterns = [
    path('', ProductsView.as_view())
]
