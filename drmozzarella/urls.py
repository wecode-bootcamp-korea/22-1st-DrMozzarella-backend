from django.urls import path, include

urlpatterns = [
    path('home'     , include('home.urls')),
    path('accounts' , include('accounts.urls')),
    path('orders'   , include('orders.urls')),
    path('comments' , include('comments.urls')),
    path('products' , include('products.urls')),
]
