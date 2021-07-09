from django.urls import path, include


urlpatterns = [
    path('events', include('events.urls')),
    path('accounts', include('accounts.urls')),
    path("products", include("products.urls"))
]
