from django.urls    import path, include

from products.views import MenuView, CategoryView


urlpatterns = [
    path('accounts' , include('accounts.urls')),
    path('orders'   , include('orders.urls')),
    path('events'   , include('events.urls')),
    path('menus'    , MenuView.as_view()),
    path("products" , include("products.urls")),
    path("categories/<int:category_id>", CategoryView.as_view())
]

