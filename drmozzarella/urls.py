from django.urls    import path, include

from products.views import MenuView, CategoryView

urlpatterns = [
    path('events'                       , include('events.urls')),
    path('accounts'                     , include('accounts.urls')),
    path('products'                     , include('products.urls')),
    path('orders'                       , include('orders.urls')),
    path('menus'                        , MenuView.as_view()),
    path("categories/<int:category_id>" , CategoryView.as_view())
]
