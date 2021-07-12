from django.urls import path, include

urlpatterns = [
    path('accounts' , include('accounts.urls')),
    path('orders'   , include('orders.urls'))
    path('events'   , include('events.urls')),
]
