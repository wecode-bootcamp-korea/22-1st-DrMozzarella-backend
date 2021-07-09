from django.urls import path
from products.views import CategoryView    

urlpatterns = [
    path('/categories', CategoryView.as_view())
]
