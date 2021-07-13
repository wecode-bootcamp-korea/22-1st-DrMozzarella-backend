from django.urls    import path, include

from products.views import MenuView


urlpatterns = [
    path('events'   , include('events.urls')),
    path('accounts' , include('accounts.urls')),
    path('orders'   , include('orders.urls')),
    path('menus'    , MenuView.as_view()),
    path("products" , include("products.urls"))
]
