from django.urls    import path, include

from products.views import MenuView

urlpatterns = [
    path('accounts' , include('accounts.urls')),
    path('orders'   , include('orders.urls')),
    path('events'   , include('events.urls')),
    path('menus'    , MenuView.as_view()),
    path('accounts' , include('accounts.urls')),
]
