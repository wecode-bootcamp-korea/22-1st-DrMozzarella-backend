from django.urls import path

from products.views import CategoryView, ProductView

urlpatterns = [
    path(''                  , CategoryView.as_view()),
    path('/<int:product_id>' , ProductView.as_view()),
]

