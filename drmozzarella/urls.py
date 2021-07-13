from django.urls    import path, include

from products.views import MenuView


urlpatterns = [
    path('menus'    , MenuView.as_view()),
    path('events', include('events.urls')),
    path('accounts', include('accounts.urls')),
    path("products", include("products.urls"))
]
